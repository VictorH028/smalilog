"""Inyector de hooks sobre un archivo Smali."""
from __future__ import annotations

import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from ._codegen import generate_d_log, generate_hook_enter, generate_hook_exit
from ._colors import Color, _c, log_error, log_info, log_ok, log_warn
from ._emit import _regnum
from ._highlight import highlight_line
from ._smali_model import SmaliMethod, normalize_reg
from ._smali_parser import parse_class_name, parse_smali_file


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class HookInjector:
    MARKER_ENTER = "Hook ENTER inyectado"
    MARKER_EXIT = "Hook EXIT inyectado"
    MARKER_D = "Log D inyectado"

    def __init__(self, file_path, remote_logger_class: str):
        self.original_path = Path(file_path)
        self.file_path = Path(file_path)
        self.remote_logger_class = remote_logger_class
        self.lines: list[str] = []
        self.methods: list[SmaliMethod] = []
        self.class_name: str | None = None
        self.target: SmaliMethod | None = None
        self.pending_registers: int | None = None
        self._plan_base: int | None = None

    # ---------- carga ----------

    def load(self) -> bool:
        if not self.file_path.exists():
            log_error(f"Archivo no encontrado: {self.file_path}")
            return False
        content = self.file_path.read_text(encoding="utf-8-sig")
        self.lines, self.methods = parse_smali_file(content)
        self.class_name = parse_class_name("\n".join(self.lines))
        return True

    def resolve_method(self, name: str, signature: str | None = None) -> bool:
        self.target = None
        self.pending_registers = None
        self._plan_base = None

        cands = [m for m in self.methods if m.name == name]
        if signature:
            cands = [m for m in cands if signature in m.signature]

        if not cands:
            log_error(f"Método '{name}' no encontrado")
            log_info("Disponibles: " + ", ".join(m.name for m in self.methods))
            return False
        if len(cands) > 1:
            log_error(f"'{name}' está sobrecargado ({len(cands)} versiones). "
                      f"Usa --signature para desambiguar:")
            for c in cands:
                print(f"      {c.name}{c.signature}")
            return False

        self.target = cands[0]
        if not self.target.has_body:
            log_error(f"'{self.target.name}' no tiene cuerpo "
                      f"(abstract/native): nada que instrumentar")
            return False
        return True

    # ---------- helpers de línea ----------

    def _find_registers_line(self) -> int | None:
        m = self.target
        for i in range(m.start_line + 1, m.end_line + 1):
            if re.match(r"\s*\.(registers|locals)\s+\d+", self.lines[i]):
                return i
        return None

    def _find_end_method_line(self, m: SmaliMethod | None = None) -> int | None:
        m = m or self.target
        for i in range(m.start_line, len(self.lines)):
            if self.lines[i].strip().startswith(".end method"):
                return i
        return None

    def _body_contains(self, marker: str) -> bool:
        end = self._find_end_method_line()
        if end is None:
            end = self.target.end_line
        return any(marker in self.lines[i]
                   for i in range(self.target.start_line, end + 1))

    def _method_id(self) -> str:
        m = self.target
        cls = self.class_name or "LUnknown;"
        return f"{cls}->{m.name}{m.signature}"

    # ---------- planificación ----------

    def _plan(self, need: int) -> list[str] | None:
        m = self.target
        if self._plan_base is None:
            self._plan_base = m.total_regs

        temps = [f"v{self._plan_base + k}" for k in range(need)]
        if max(_regnum(t) for t in temps) > 255:
            log_error("Método demasiado grande (>255 regs): const-string y "
                      "move-result no soportan índices mayores")
            return None

        new_total = self._plan_base + need
        if self.pending_registers is None or new_total > self.pending_registers:
            self.pending_registers = new_total

        m.directive = "registers"
        m.registers_value = self.pending_registers
        return temps

    def _write_registers_to_lines(self) -> None:
        if self.pending_registers is None:
            return
        idx = self._find_registers_line()
        if idx is None:
            self.lines.insert(self.target.start_line + 1,
                              f"    .registers {self.pending_registers}")
            log_info(f"Añadida directiva .registers {self.pending_registers}")
            return
        self.lines[idx] = re.sub(
            r"\.(registers|locals)\s+\d+",
            f".registers {self.pending_registers}",
            self.lines[idx],
        )
        log_info(f"Registros aplicados: .registers {self.pending_registers}")

    # ---------- visualización ----------

    def show_method(self, method: SmaliMethod | None = None,
                    color: bool | None = None, line_numbers: bool = True,
                    style: str = "default") -> bool:
        from ._colors import use_color_default
        m = method or self.target
        if m is None:
            log_error("No hay método seleccionado")
            return False
        if color is None:
            color = use_color_default()

        def C(code: str, s: str) -> str:
            return f"{code}{s}{Color.RESET}" if color else str(s)

        end = self._find_end_method_line(m)
        if end is None:
            end = m.end_line
        if not m.has_body:
            log_warn("El método no tiene cuerpo (abstract/native)")

        body = self.lines[m.start_line:end + 1]
        first_num = m.start_line + 1
        width = max(len(str(end + 1)), 3)
        cls = self.class_name or "L?;"

        print()
        print(C(Color.BOLD + Color.CYAN, "━" * 72))
        print(C(Color.BOLD, f"{cls}->")
              + C(Color.BOLD + Color.YELLOW, f"{m.name}{m.signature}"))
        info = (f".{m.directive} {m.registers_value}"
                + (f"  (total {m.total_regs})"
                   if m.directive == "locals" else "")
                + f"  ·  {'static' if m.is_static() else 'instance'}"
                + f"  ·  {len(m.parameters)} params"
                + f"  ·  {len(body)} líneas")
        print(C(Color.DIM, info))
        print(C(Color.BOLD + Color.CYAN, "━" * 72))

        in_hook = False
        for off, raw in enumerate(body):
            num = first_num + off
            s = raw.strip()

            if s.startswith("#") and "inyectado" in s:
                in_hook = True

            if in_hook:
                gutter = C(Color.GREEN, "+")
            else:
                gutter = C(Color.DIM, "│") if color else "|"

            if line_numbers:
                prefix = f"{C(Color.DIM, f'{num:>{width}}')} {gutter} "
            else:
                prefix = f"{gutter} "

            print(prefix + highlight_line(raw, color=color, style=style))

            if in_hook and re.fullmatch(r"#\s*=+\s*", s):
                in_hook = False

        hooks = sum(1 for r in body
                    if r.strip().startswith("#") and "inyectado" in r)
        if hooks:
            print(C(Color.DIM, "─" * 72))
            print(C(Color.GREEN, f"  ▸ {hooks} bloque(s) inyectado(s)"))
        print()
        return True

    # ---------- inyección ----------

    def inject_enter(self) -> bool:
        m = self.target
        if self._body_contains(self.MARKER_ENTER):
            log_warn(f"Hook ENTER ya presente en {m.name}; se omite")
            return True

        if m.is_static():
            if m.parameters:
                arg_name, arg_desc, arg_sym = "arg0", m.parameters[0], "p0"
            else:
                arg_name, arg_desc, arg_sym = "null", None, None
        else:
            arg_name = "this"
            arg_desc = self.class_name or "Ljava/lang/Object;"
            arg_sym = "p0"

        temps = self._plan(need=3)
        if temps is None:
            return False

        arg_reg = normalize_reg(arg_sym, m) if arg_sym else None

        idx = self._find_registers_line()
        if idx is None:
            idx = m.start_line
            self.lines.insert(idx + 1,
                              f"    .registers {self.pending_registers}")
            idx += 1

        block = [
            f"    # {self.MARKER_ENTER} - {_utc_now_iso()}",
            generate_hook_enter(self._method_id(), arg_name,
                                arg_desc, arg_reg, temps,
                                self.remote_logger_class),
            "",
        ]
        self.lines[idx + 1:idx + 1] = block

        log_ok(f"Hook ENTER inyectado en {m.name} (temps: {temps})")
        return True

    def inject_exit(self) -> bool:
        m = self.target
        if self._body_contains(self.MARKER_EXIT):
            log_warn(f"Hook EXIT ya presente en {m.name}; se omite")
            return True

        end_idx = self._find_end_method_line()
        if end_idx is None:
            log_error("No se encontró .end method")
            return False

        ret_indices = [
            i for i in range(m.start_line + 1, end_idx)
            if re.match(r"return(?:-object|-wide|-void)?(?:\s|$)",
                        self.lines[i].strip())
        ]
        if not ret_indices:
            log_warn(f"No se encontraron returns en {m.name}")
            return False

        temps = self._plan(need=2)
        if temps is None:
            return False

        count = 0
        for idx in reversed(ret_indices):
            line = self.lines[idx].strip()

            if line == "return-void":
                code = generate_hook_exit(self._method_id(), line, None,
                                          temps, m.return_type,
                                          self.remote_logger_class)
                self.lines[idx:idx] = ["", code]
                count += 1
                continue

            mt = re.match(r"return(-object|-wide)?\s+(\S+)$", line)
            if not mt:
                log_warn(f"Return no reconocido, se omite: '{line}'")
                continue
            kind = mt.group(1) or ""
            reg = normalize_reg(mt.group(2), m)
            code = generate_hook_exit(self._method_id(), "return" + kind,
                                      reg, temps, m.return_type,
                                      self.remote_logger_class)
            self.lines[idx:idx] = ["", code]
            count += 1

        log_ok(f"Hook EXIT inyectado en {m.name} "
               f"({count} returns, temps: {temps})")
        return True

    def inject_d(self, tag: str, message: str) -> bool:
        m = self.target
        if self._body_contains(self.MARKER_D):
            log_warn(f"Log D ya presente en {m.name}; se omite")
            return True

        temps = self._plan(need=2)
        if temps is None:
            return False

        idx = self._find_registers_line()
        if idx is None:
            idx = m.start_line
            self.lines.insert(idx + 1,
                              f"    .registers {self.pending_registers}")
            idx += 1

        block = [
            f"    # {self.MARKER_D} - {_utc_now_iso()}",
            generate_d_log(tag, message, temps, self.remote_logger_class),
            "",
        ]
        self.lines[idx + 1:idx + 1] = block

        log_ok(f'Log d("{tag}", "{message}") inyectado en {m.name} '
               f"(temps: {temps})")
        return True

    def save(self, output: str | None = None, backup: bool = True) -> None:
        self._write_registers_to_lines()
        out_path = Path(output) if output else self.original_path

        if backup:
            bak = self.original_path.with_suffix(".smali.bak")
            shutil.copy2(self.original_path, bak)
            log_info(f"Backup guardado en: {bak}")

        out_path.write_text("\n".join(self.lines) + "\n", encoding="utf-8")
        log_ok(f"Archivo guardado: {out_path}")
