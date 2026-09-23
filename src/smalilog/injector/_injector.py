"""Inyector de hooks sobre un archivo Smali."""
from __future__ import annotations

import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from smalilog.smali import generate_d_log, generate_hook_enter, generate_hook_exit
from smalilog.ui import Color, log_error, log_info, log_ok, log_warn
from smalilog.ui import highlight_line, use_color_default
from smalilog.smali import plan_hook_registers
from smalilog.smali import SmaliMethod, normalize_reg, parse_class_name, parse_smali_file, is_reference
from smalilog.emit._emit import _regnum


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

    # ---------- carga ----------

    def load(self) -> bool:
        if not self.file_path.exists():
            log_error(f"Archivo no encontrado: {self.file_path}")
            return False
        content = self.file_path.read_text(encoding="utf-8-sig")
        self.lines, self.methods = parse_smali_file(content)
        self.class_name = parse_class_name("\n".join(self.lines))
        return True
    
    def _require_target(self) -> SmaliMethod:
        """Devuelve self._require_target() garantizando que no es None."""
        if self._require_target() is None:
            raise RuntimeError(
                "HookInjector: no hay método resuelto. "
                "Llama a resolve_method() primero."
            )
        return self._require_target()

    def resolve_method(self, name: str, signature: str | None = None) -> bool:
        self.target = None
        self.pending_registers = None

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
        if not self._require_target().has_body:
            log_error(f"'{self._require_target().name}' no tiene cuerpo "
                      f"(abstract/native): nada que instrumentar")
            return False
        return True

    # ---------- helpers de línea ----------

    def _find_registers_line(self) -> int | None:
        m = self._require_target()
        for i in range(m.start_line + 1, m.end_line + 1):
            if re.match(r"\s*\.(registers|locals)\s+\d+", self.lines[i]):
                return i
        return None

    def _find_end_method_line(self, m: SmaliMethod | None = None) -> int | None:
        m = m or self._require_target()
        for i in range(m.start_line, len(self.lines)):
            if self.lines[i].strip().startswith(".end method"):
                return i
        return None

    def _body_contains(self, marker: str) -> bool:
        end = self._find_end_method_line()
        if end is None:
            end = self._require_target().end_line
        return any(marker in self.lines[i]
                   for i in range(self._require_target().start_line, end + 1))

    def _method_id(self) -> str:
        m = self._require_target()
        cls = self.class_name or "LUnknown;"
        return f"{cls}->{m.name}{m.signature}"

    # ---------- planificación centralizada ----------

    def _apply_plan(self, need: int) -> list[str] | None:
        """Aplica la planificación de registros universal usando _register_planner.py"""
        m = self._require_target()
        plan = plan_hook_registers(m, need=need)
        temps = plan["temps"]

        if max(_regnum(t) for t in temps) > 255:
            log_error("Método demasiado grande (>255 regs): no se pueden inyectar hooks")
            return None

        # Guardamos el total acumulado necesario para este método
        new_total = plan["new_total_regs"]
        if self.pending_registers is None or new_total > self.pending_registers:
            self.pending_registers = new_total

        return temps

    def _write_registers_to_lines(self) -> None:
        if self.pending_registers is None or self._require_target() is None:
            return
        idx = self._find_registers_line()
        if idx is None:
            self.lines.insert(self._require_target().start_line + 1,
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
        m = method or self._require_target()
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

        body = self.lines[m.start_line:end + 1]
        first_num = m.start_line + 1
        width = max(len(str(end + 1)), 3)
        cls = self.class_name or "L?;"

        print()
        print(C(Color.BOLD + Color.CYAN, "━" * 72))
        print(C(Color.BOLD, f"{cls}->")
              + C(Color.BOLD + Color.YELLOW, f"{m.name}{m.signature}"))
        info = (f".{m.directive} {m.registers_value}"
                + (f"  (total {m.total_regs})" if m.directive == "locals" else "")
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

            gutter = C(Color.GREEN, "+") if in_hook else (C(Color.DIM, "│") if color else "|")
            prefix = f"{C(Color.DIM, f'{num:>{width}}')} {gutter} " if line_numbers else f"{gutter} "

            print(prefix + highlight_line(raw, color=color, style=style))

            if in_hook and re.fullmatch(r"#\s*=+\s*", s):
                in_hook = False

        hooks = sum(1 for r in body if r.strip().startswith("#") and "inyectado" in r)
        if hooks:
            print(C(Color.DIM, "─" * 72))
            print(C(Color.GREEN, f"  ▸ {hooks} bloque(s) inyectado(s)"))
        print()
        return True

    # ---------- inyección ----------

    def inject_enter(self) -> bool:
        m = self._require_target()
        if self._body_contains(self.MARKER_ENTER):
            log_warn(f"Hook ENTER ya presente en {m.name}; se omite")
            return True

        if m.parameters:
            arg_name = "arg0"
            arg_desc = m.parameters[0]
            arg_sym = "p0" if m.is_static() else "p1"
        else:
            if m.is_static():
                arg_name = "null"
                arg_desc = None
                arg_sym = None
            else:
                arg_name = "this"
                arg_desc = self.class_name or "Ljava/lang/Object;"
                arg_sym = "p0"

        needs_boxing = (arg_desc is None) or (not is_reference(arg_desc))
        needed_temps = 3 if needs_boxing else 2

        temps = self._apply_plan(need=needed_temps)
        if temps is None:
            return False

        idx = self._find_registers_line()
        if idx is None:
            idx = m.start_line

        block = [
            f"    # {self.MARKER_ENTER} - {_utc_now_iso()}",
            generate_hook_enter(self._method_id(), arg_name,
                                arg_desc, arg_sym, temps,
                                self.remote_logger_class),
            "",
        ]
        self.lines[idx + 1:idx + 1] = block
        self._write_registers_to_lines()

        log_ok(f"Hook ENTER inyectado en {m.name} (temps: {temps}, arg: {arg_sym})")
        return True

    def inject_exit(self) -> bool:
        m = self._require_target()    
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

        # 1. PLANIFICAR Y APLICAR REGISTROS DE INMEDIATO EN EL MODELO
        temps = self._apply_plan(need=2)
        if temps is None:
            return False

        # Actualizar el modelo del método ANTES de evaluar normalizaciones de pX -> vY
        assert self.pending_registers is not None
        m.directive = "registers"
        m.registers_value = self.pending_registers

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
            raw_reg = mt.group(2)

            # 2. RESOLVER REGISTRO TARGET (Si era p0, con m.registers_value ya actualizado, devuelve el vY real)
            reg = normalize_reg(raw_reg, m)

            code = generate_hook_exit(self._method_id(), "return" + kind,
                                      reg, temps, m.return_type,
                                      self.remote_logger_class)
            self.lines[idx:idx] = ["", code]
            count += 1

        self._write_registers_to_lines()
        log_ok(f"Hook EXIT inyectado en {m.name} ({count} returns, temps: {temps})")
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
     

    def inject_lifecycle_tracker(self) -> bool:
        """Inyecta LifecycleTracker.init(this) justo después de invoke-super onCreate."""
        m = self._require_target()
        if m is None or m.name != "onCreate":
            log_error("El método objetivo debe ser 'onCreate'")
            return False

        full_marker = "Lcom/deadnote/LifecycleTracker;->init("
        if self._body_contains(full_marker):
            log_warn(f"LifecycleTracker ya inyectado en {m.name}; se omite")
            return True

        end_idx = self._find_end_method_line()
        if end_idx is None:
            log_error("No se encontró .end method")
            return False

        # Detectar si el método es estático (no hay p0)
        if m.is_static():
            log_error("onCreate no puede ser estático")
            return False

        # Buscar invoke-super a onCreate de Application o Activity
        super_idx = None
        super_sig = None
        for i in range(m.start_line + 1, end_idx):
            line = self.lines[i].strip()
            if not line.startswith("invoke-super"):
                continue
            if "->onCreate()V" in line:
                super_sig = "()V"
            elif "->onCreate(Landroid/os/Bundle;)V" in line:
                super_sig = "(Landroid/os/Bundle;)V"
            else:
                continue
            super_idx = i
            break

        if super_idx is None:
            log_error("No se encontró invoke-super a onCreate() en el método")
            return False

        # Verificar que p0 sea Application antes de pasar como Application
        # (si es Activity con onCreate(Bundle), no forzamos Application)
        if super_sig == "()V":
            # Application.onCreate() -> p0 es Application
            arg_type = "Landroid/app/Application;"
        else:
            # Activity.onCreate(Bundle) -> p0 es Activity, NO Application
            log_error("LifecycleTracker solo se inyecta en Application.onCreate()")
            return False

        block = [
            f"    # LifecycleTracker inyectado - {_utc_now_iso()}",
            f"    invoke-static {{p0}}, Lcom/deadnote/LifecycleTracker;->init({arg_type})V",
            "",
        ]

        self.lines[super_idx + 1:super_idx + 1] = block
        log_ok(f"LifecycleTracker.init(p0) inyectado exitosamente en {m.name}")
        return True 
