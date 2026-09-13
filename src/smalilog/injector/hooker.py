"""
smalilog.injector.hooker
Inyecta hooks de observación en archivos Smali.

API programática:
    from smalilog.injector.hooker import run_hooker
    run_hooker(["archivo.smali", "--method", "Sf", "--action", "both"])

Notas de diseño:
    - SIEMPRE se expande `.registers` y los temporales se toman de la
      ventana de registros recién creada (bajo los parámetros). Eso
      garantiza que nunca se pisan locales en uso ni registros de retorno
      sin necesidad de análisis de liveness.
    - Los archivos con `.locals` se convierten a `.registers` al guardar
      (semánticamente equivalentes, y evita bugs de aritmética).
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# ============================================================
# CONFIGURACIÓN
# ============================================================

REMOTE_LOGGER_CLASS = "Lcom/deadnote/RemoteLogger;"

# ============================================================
# COLORES (se desactivan sin TTY o con NO_COLOR)
# ============================================================

class Color:
    RED = "\033[91m"; GREEN = "\033[92m"; YELLOW = "\033[93m"
    BLUE = "\033[94m"; CYAN = "\033[96m"; BOLD = "\033[1m"; RESET = "\033[0m"

_USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def _c(code: str, msg: str) -> str:
    return f"{code}{msg}{Color.RESET}" if _USE_COLOR else str(msg)


def log_info(msg):  print(f"{_c(Color.BLUE, '[INFO]')} {msg}")
def log_ok(msg):    print(f"{_c(Color.GREEN, '[OK]')} {msg}")
def log_warn(msg):  print(f"{_c(Color.YELLOW, '[WARN]')} {msg}")
def log_error(msg): print(f"{_c(Color.RED, '[ERROR]')} {msg}")


def log_header(msg):
    bar = "=" * 60
    print(f"\n{_c(Color.BOLD + Color.CYAN, bar)}")
    print(_c(Color.BOLD + Color.CYAN, msg))
    print(_c(Color.BOLD + Color.CYAN, bar) + "\n")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


# ============================================================
# TIPOS SMALI
# ============================================================

def _type_size(desc: str) -> int:
    """J (long) y D (double) ocupan 2 registros."""
    return 2 if desc in ("J", "D") else 1


def is_reference(desc: str) -> bool:
    return desc[:1] in ("L", "[")


def parse_type_list(params_str: str) -> list[str]:
    params: list[str] = []
    i = 0
    while i < len(params_str):
        c = params_str[i]
        if c == "L":
            end = params_str.index(";", i)
            params.append(params_str[i:end + 1]); i = end + 1
        elif c == "[":
            start = i
            while i < len(params_str) and params_str[i] == "[":
                i += 1
            if i < len(params_str) and params_str[i] == "L":
                end = params_str.index(";", i)
                params.append(params_str[start:end + 1]); i = end + 1
            else:
                params.append(params_str[start:i + 1]); i += 1
        else:
            params.append(c); i += 1
    return params


def _params_raw(signature: str) -> str:
    m = re.search(r"\((.*?)\)", signature)
    return m.group(1) if m else ""


def _return_raw(signature: str) -> str:
    m = re.search(r"\)(.+)$", signature)
    return m.group(1) if m else "V"


# ============================================================
# MODELO
# ============================================================

@dataclass
class SmaliMethod:
    name: str
    signature: str
    access: str
    directive: str            # 'registers' | 'locals' (tal cual en el archivo)
    registers_value: int      # número tal cual aparece en el .smali
    start_line: int
    end_line: int             # índice de '.end method' (o última línea útil)
    has_body: bool = True

    parameters: list[str] = field(init=False)
    return_type: str = field(init=False)

    def __post_init__(self):
        self.parameters = parse_type_list(_params_raw(self.signature))
        self.return_type = _return_raw(self.signature)

    def is_static(self) -> bool:
        return "static" in self.access.split()

    @property
    def n_param_regs(self) -> int:
        return count_parameter_registers(self)

    @property
    def total_regs(self) -> int:
        """Total de registros (v0..vN-1) con la semántica correcta."""
        if self.directive == "locals":
            return self.registers_value + self.n_param_regs
        return self.registers_value

    def __repr__(self):
        return f"<SmaliMethod {self.name}{self.signature}>"


def count_parameter_registers(method: SmaliMethod) -> int:
    total = 0 if method.is_static() else 1  # this
    for p in method.parameters:
        total += _type_size(p)
    return total


def param_register_offsets(method: SmaliMethod) -> list[tuple[int, int, int]]:
    """[(p_index, v_inicial, tamaño), ...] — respeta anchos wide.

    pN indexa PARÁMETROS, no registros: con (JI), p1 empieza en
    base+2, no en base+1.
    """
    base = method.total_regs - count_parameter_registers(method)
    out, cur = [], base
    for i, p in enumerate(method.parameters):
        size = _type_size(p)
        out.append((i, cur, size))
        cur += size
    return out


def normalize_reg(reg: str, method: SmaliMethod) -> str:
    """Convierte 'pN' a 'vX' con la numeración ACTUAL del método."""
    reg = reg.strip()
    if reg.startswith("v") and reg[1:].isdigit():
        return reg
    if reg.startswith("p") and reg[1:].isdigit():
        idx = int(reg[1:])
        offs = param_register_offsets(method)
        if 0 <= idx < len(offs):
            return f"v{offs[idx][1]}"
        log_warn(f"p{idx} fuera de rango en {method.name}")
    return reg


# ============================================================
# PARSING
# ============================================================

def _parse_method_line(line: str):
    """Devuelve (access, name, signature) o None.

    Acepta líneas sin flags de acceso: '.method foo(I)V'.
    """
    rest = line[len(".method"):].strip()
    p = rest.find("(")
    if p == -1:
        return None
    head = rest[:p].split()
    if not head:
        return None
    return " ".join(head[:-1]), head[-1], rest[p:]


def parse_smali_file(content: str):
    lines = content.splitlines()
    methods: list[SmaliMethod] = []
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith(".method"):
            parsed = _parse_method_line(stripped)
            start = i
            j = i + 1
            end = len(lines) - 1
            has_body = False
            directive, reg_val = "registers", 0
            while j < len(lines):
                s = lines[j].strip()
                if s.startswith(".end method"):
                    has_body, end = True, j
                    break
                if s.startswith(".method"):
                    # método abstract/native: sin cuerpo. NO absorber
                    # el siguiente método (bug del parser original).
                    end = j - 1
                    break
                mm = re.match(r"\.(registers|locals)\s+(\d+)", s)
                if mm:
                    directive, reg_val = mm.group(1), int(mm.group(2))
                j += 1
            if parsed:
                access, name, signature = parsed
                methods.append(SmaliMethod(
                    name, signature, access, directive, reg_val,
                    start, end, has_body,
                ))
            i = end
        i += 1
    return lines, methods


def parse_class_name(content: str) -> str | None:
    for line in content.splitlines():
        s = line.strip()
        if s.startswith(".class"):
            parts = s.split()
            if parts:
                return parts[-1]  # Lcom/foo/Bar;
    return None


# ============================================================
# PLANIFICACIÓN DE REGISTROS (siempre expandir: seguro)
# ============================================================

def plan_hook_registers(method: SmaliMethod, need: int = 2) -> dict:
    """Plan PURE (no muta): expande y devuelve la ventana fresca.

    Los registros frescos v(total)..v(total+need-1) quedan justo
    debajo de los parámetros y están garantizados sin usar.
    """
    base = method.total_regs
    return {
        "expand_to": base + need,
        "temps": [f"v{base + k}" for k in range(need)],
    }


# ============================================================
# HELPERS DE EMISIÓN (respetan límites 4-bit/8-bit de Dalvik)
# ============================================================

def _regnum(r: str) -> int:
    return int(r[1:])


def _invoke_static(regs: list[str], target: str) -> str:
    nums = [_regnum(r) for r in regs]
    if len(regs) == 1:
        if nums[0] <= 15:
            return f"invoke-static {{{regs[0]}}}, {target}"
        return f"invoke-static/range {{{regs[0]} .. {regs[0]}}}, {target}"
    if max(nums) <= 15:
        return f"invoke-static {{{', '.join(regs)}}}, {target}"
    if nums == list(range(nums[0], nums[0] + len(nums))):
        return f"invoke-static/range {{{regs[0]} .. {regs[-1]}}}, {target}"
    raise ValueError(f"Registros no contiguos para /range: {regs}")


def _move_object(dst: str, src: str) -> str:
    if _regnum(dst) > 15 or _regnum(src) > 15:
        return f"move-object/16 {dst}, {src}"
    return f"move-object {dst}, {src}"


def _const_null(reg: str) -> str:
    if _regnum(reg) <= 15:
        return f"const/4 {reg}, 0x0"
    return f"const/16 {reg}, 0x0"


_WIDE_BOX = {
    "J": "Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;",
    "D": "Ljava/lang/Double;->valueOf(D)Ljava/lang/Double;",
}


def _box_scalar(desc: str, src: str, dst: str) -> list[str]:
    """Boxea un escalar smali a Object (instrucciones ya emitidas)."""
    if desc == "F":
        target = "Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;"
    elif desc in _WIDE_BOX:
        target = _WIDE_BOX[desc]
    else:  # I, Z, B, C, S: en el registro ya son int
        target = "Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;"
    return [_invoke_static([src], target), f"move-result-object {dst}"]


def indent(code: str, spaces: int = 4) -> str:
    prefix = " " * spaces
    return "\n".join(
        prefix + ln if ln.strip() else ln for ln in code.split("\n")
    )


# ============================================================
# GENERADORES
# ============================================================

def generate_hook_enter(func_name, arg_name, arg_desc, arg_register, temps):
    """Boxea el argumento según su TIPO real (no move-object a ciegas)."""
    t_name, t_argname, t_val = temps
    lines = [
        "# ========== HOOK ENTER ==========",
        f'const-string {t_name}, "{func_name}"',
        f'const-string {t_argname}, "{arg_name}"',
    ]
    if arg_desc is None:                       # static sin parámetros
        lines.append(_const_null(t_val))       # NO leer registros basura
    elif is_reference(arg_desc):
        lines.append(_move_object(t_val, arg_register))
    else:
        lines += _box_scalar(arg_desc, arg_register, t_val)
    lines += [
        _invoke_static(
            [t_name, t_argname, t_val],
            f"{REMOTE_LOGGER_CLASS}->hookEnter("
            f"Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V",
        ),
        "# ================================",
    ]
    return indent("\n".join(lines))


def generate_hook_exit(func_name, return_line, return_reg, temps, ret_type):
    """Boxea el valor de retorno según instrucción + tipo del método."""
    t_name, t_val = temps
    target = (f"{REMOTE_LOGGER_CLASS}->hookExit("
              f"Ljava/lang/String;Ljava/lang/Object;)V")
    head = [
        "# ========== HOOK EXIT ==========",
        f'const-string {t_name}, "{func_name}"',
    ]

    if return_line == "return-void" or return_reg is None:
        body = [f'const-string {t_val}, "void"']
        invoke = _invoke_static(
            [t_name, t_val],
            f"{REMOTE_LOGGER_CLASS}->d(Ljava/lang/String;Ljava/lang/String;)V",
        )
        return indent("\n".join(head + body + [invoke, "# ================================"]))

    if return_line.startswith("return-object"):
        body = [_move_object(t_val, return_reg)]
    elif return_line.startswith("return-wide"):
        body = _box_scalar("D" if ret_type == "D" else "J", return_reg, t_val)
    else:  # return (4-bit): Z/B/C/S/I → Integer, F → Float
        body = _box_scalar("F" if ret_type == "F" else "I", return_reg, t_val)

    return indent("\n".join(head + body + [
        _invoke_static([t_name, t_val], target),
        "# ================================",
    ]))


def generate_d_log(tag, message, temps):
    t_tag, t_msg = temps
    return indent("\n".join([
        "# ========== LOG D ==========",
        f'const-string {t_tag}, "{tag}"',
        f'const-string {t_msg}, "{message}"',
        _invoke_static(
            [t_tag, t_msg],
            f"{REMOTE_LOGGER_CLASS}->d(Ljava/lang/String;Ljava/lang/String;)V",
        ),
        "# ============================",
    ]))


# ============================================================
# INYECTOR
# ============================================================

class HookInjector:
    MARKER_ENTER = "# Hook ENTER inyectado"
    MARKER_EXIT = "# Hook EXIT inyectado"
    MARKER_D = "# Log D inyectado"

    def __init__(self, file_path):
        self.original_path = Path(file_path)
        self.file_path = Path(file_path)
        self.lines: list[str] = []
        self.methods: list[SmaliMethod] = []
        self.class_name: str | None = None
        self.target: SmaliMethod | None = None
        self.pending_registers: int | None = None
        self._plan_base: int | None = None   # total ORIGINAL del método

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
        """Resolución perezosa: permite --list sin --method."""
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

    def _find_end_method_line(self) -> int | None:
        for i in range(self.target.start_line, len(self.lines)):
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

    # ---------- planificación (con memoria de la ventana fresca) ----------

    def _plan(self, need: int) -> list[str] | None:
        """Ventana de temps fresca, compartida entre enter/exit/d.

        El primer plan fija la base (total ORIGINAL); los siguientes
        reutilizan la misma ventana en vez de seguir expandiendo.
        """
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

        # Reflejar YA en memoria para que normalize_reg('pN') use el
        # mapeo final (los pN se desplazan con la expansión).
        m.directive = "registers"
        m.registers_value = self.pending_registers
        return temps

    def _write_registers_to_lines(self) -> None:
        if self.pending_registers is None:
            return
        idx = self._find_registers_line()
        if idx is None:
            # Sin directiva: insertamos una justo tras .method
            self.lines.insert(self.target.start_line + 1,
                              f"    .registers {self.pending_registers}")
            log_info(f"Añadida directiva .registers {self.pending_registers}")
            return
        # Convierte .locals → .registers con el total correcto
        self.lines[idx] = re.sub(
            r"\.(registers|locals)\s+\d+",
            f".registers {self.pending_registers}",
            self.lines[idx],
        )
        log_info(f"Registros aplicados: .registers {self.pending_registers}")

    # ---------- inyección ----------

    def inject_enter(self) -> bool:
        m = self.target
        if self._body_contains(self.MARKER_ENTER):
            log_warn(f"Hook ENTER ya presente en {m.name}; se omite")
            return True

        # Qué observamos en la entrada
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

        # Inserción como bloque: comentario ANTES del código (bug de orden)
        block = [
            f"    # {self.MARKER_ENTER} - {_utc_now_iso()}",
            generate_hook_enter(self._method_id(), arg_name,
                                arg_desc, arg_reg, temps),
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

        # Inyectamos de abajo hacia arriba; los temps son frescos, por lo
        # que NUNCA pisan el registro que devuelve cada `return`.
        count = 0
        for idx in reversed(ret_indices):
            line = self.lines[idx].strip()

            if line == "return-void":
                code = generate_hook_exit(self._method_id(), line, None,
                                          temps, m.return_type)
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
                                      reg, temps, m.return_type)
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

        block = [
            f"    # {self.MARKER_D} - {_utc_now_iso()}",
            generate_d_log(tag, message, temps),
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
            # Backup SIEMPRE del original (bug con -o: antes se copiaba
            # un archivo de salida que aún no existía).
            bak = self.original_path.with_suffix(".smali.bak")
            shutil.copy2(self.original_path, bak)
            log_info(f"Backup guardado en: {bak}")

        out_path.write_text("\n".join(self.lines) + "\n", encoding="utf-8")
        log_ok(f"Archivo guardado: {out_path}")


# ============================================================
# ANALYZE
# ============================================================

def analyze_method(method: SmaliMethod, class_name: str | None = None):
    log_header(f"Método: {method.name}"
               + ("" if method.has_body else "  (SIN CUERPO)"))
    print(f"  {_c(Color.CYAN, 'Clase:')}     {class_name or '?'}")
    print(f"  {_c(Color.CYAN, 'Signature:')} {method.signature}")
    print(f"  {_c(Color.CYAN, 'Access:')}    {method.access}")
    print(f"  {_c(Color.CYAN, 'Directiva:')} "
          f".{method.directive} {method.registers_value}"
          + (f"  (total real: {method.total_regs})"
             if method.directive == "locals" else ""))

    n = count_parameter_registers(method)
    base = method.total_regs - n
    print(f"  {_c(Color.CYAN, 'Params:')}     {n} regs "
          f"(v{base}..v{method.total_regs - 1})")

    if method.parameters:
        print(f"  {_c(Color.CYAN, 'Mapeo p → v:')} "
              f"(respeta anchos wide)")
        for (i, start, size), p in zip(param_register_offsets(method),
                                       method.parameters):
            span = f"v{start}" if size == 1 else f"v{start}-v{start + 1}"
            print(f"    p{i} → {span:<11} {p}")

    plan = plan_hook_registers(method, need=3)
    print(f"  {_c(Color.CYAN, 'Plan:')}       expandir a "
          f".registers {plan['expand_to']}, temps frescos {plan['temps']}")
    print()


# ============================================================
# CLI
# ============================================================

def build_hook_parser(prog: str = "smalilog hook") -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Inyecta hooks de observación en archivos Smali",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  smalilog hook archivo.smali --list
  smalilog hook archivo.smali --method Sf --analyze
  smalilog hook archivo.smali --method Sf --action enter
  smalilog hook archivo.smali --method Sf --action both
  smalilog hook archivo.smali --method Sf --action d --tag MiTag --message "Hola"
  smalilog hook archivo.smali --method Sf --signature "(I)V" --action both
        """,
    )
    parser.add_argument("file", nargs="?", help="Archivo Smali a procesar")
    parser.add_argument("--method", "-m", help="Nombre del método objetivo")
    parser.add_argument("--signature",
                        help="Subcadena de firma para desambiguar sobrecargas")
    parser.add_argument("--action", "-a",
                        choices=["enter", "exit", "both", "observ",
                                 "analyze", "d"],
                        default="both",
                        help="Acción (default: both)")
    parser.add_argument("--tag", default="LOG", help='Tag para acción "d"')
    parser.add_argument("--message", "--msg", default="Mensaje de log",
                        help='Mensaje para acción "d"')
    parser.add_argument("--analyze", action="store_true", help="Solo analizar")
    parser.add_argument("--list", "-l", action="store_true",
                        help="Listar métodos")
    parser.add_argument("--no-backup", action="store_true",
                        help="No crear backup")
    parser.add_argument("--output", "-o", help="Archivo de salida")
    return parser


def run_hooker(argv: list[str] | None = None,
               prog: str = "smalilog hook") -> int:
    parser = build_hook_parser(prog=prog)
    args = parser.parse_args(argv)

    if not args.file:
        parser.error("se requiere la ruta del archivo .smali")

    log_header("smalilog hook - Inyector de hooks")

    injector = HookInjector(args.file)
    if not injector.load():          # NO exige --method (bug de --list)
        return 1

    if args.list:
        log_header(f"Métodos en {args.file}")
        for m in injector.methods:
            flags = []
            if m.is_static():
                flags.append("static")
            if not m.has_body:
                flags.append("sin cuerpo")
            extra = f" [{' '.join(flags)}]" if flags else ""
            print(f"  {_c(Color.GREEN, m.name)}{m.signature} "
                  f"({m.total_regs} regs){extra}")
        return 0

    if args.analyze or args.action == "analyze":
        if not args.method:
            log_error("--analyze requiere --method")
            return 1
        if not injector.resolve_method(args.method, args.signature):
            return 1
        analyze_method(injector.target, injector.class_name)
        return 0

    if not args.method:
        log_error("Debes especificar --method (o usar --list / --analyze)")
        return 1
    if not injector.resolve_method(args.method, args.signature):
        return 1

    log_info(f"Archivo: {args.file}")
    log_info(f"Método:  {args.method}{injector.target.signature}")
    log_info(f"Acción:  {args.action}")
    analyze_method(injector.target, injector.class_name)

    if args.action == "d":
        success = injector.inject_d(args.tag, args.message)
    elif args.action == "enter":
        success = injector.inject_enter()
    elif args.action == "exit":
        success = injector.inject_exit()
    else:  # both / observ
        ok_enter = injector.inject_enter()
        ok_exit = injector.inject_exit()
        success = ok_enter and ok_exit
        if not success and (ok_enter or ok_exit):
            log_warn("Inyección parcial: revisa los mensajes anteriores")

    if not success:
        log_error("No se pudo completar la inyección")
        return 1

    injector.save(output=args.output, backup=not args.no_backup)
    log_header("INYECCIÓN COMPLETADA")
    return 0


if __name__ == "__main__":
    sys.exit(run_hooker())
