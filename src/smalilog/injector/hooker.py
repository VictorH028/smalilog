#!/usr/bin/env python3
"""
smalilog.injector.hooker
Inyecta hooks de observación en archivos Smali.

API programática:
    from smalilog.injector.hooker import run_hooker
    run_hooker(["archivo.smali", "--method", "Sf", "--action", "both"])
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path


# ============================================================
# CONFIGURACIÓN
# ============================================================

REMOTE_LOGGER_CLASS = "Lcom/deadnote/RemoteLogger;"


# ============================================================
# COLORES
# ============================================================

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def log_info(msg):  print(f"{Color.BLUE}[INFO]{Color.RESET} {msg}")
def log_ok(msg):    print(f"{Color.GREEN}[OK]{Color.RESET} {msg}")
def log_warn(msg):  print(f"{Color.YELLOW}[WARN]{Color.RESET} {msg}")
def log_error(msg): print(f"{Color.RED}[ERROR]{Color.RESET} {msg}")
def log_header(msg):
    print(f"\n{Color.BOLD}{Color.CYAN}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN}{msg}{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN}{'='*60}{Color.RESET}\n")


# ============================================================
# PARSER
# ============================================================

class SmaliMethod:
    def __init__(self, name, signature, access, registers, start_line, end_line, is_locals=False):
        self.name = name
        self.signature = signature
        self.access = access
        self.registers = registers
        self.is_locals = is_locals
        self.start_line = start_line
        self.end_line = end_line
        self.parameters = self._parse_parameters()
        self.return_type = self._parse_return_type()

    def _parse_parameters(self):
        match = re.search(r'\((.*?)\)', self.signature)
        if not match:
            return []
        params_str = match.group(1)
        params = []
        i = 0
        while i < len(params_str):
            c = params_str[i]
            if c == 'L':
                end = params_str.index(';', i)
                params.append(params_str[i:end+1])
                i = end + 1
            elif c == '[':
                start = i
                while i < len(params_str) and params_str[i] == '[':
                    i += 1
                if i < len(params_str) and params_str[i] == 'L':
                    end = params_str.index(';', i)
                    params.append(params_str[start:end+1])
                    i = end + 1
                else:
                    params.append(params_str[start:i+1])
                    i += 1
            else:
                params.append(c)
                i += 1
        return params

    def _parse_return_type(self):
        match = re.search(r'\)(.+)$', self.signature)
        return match.group(1) if match else 'V'

    def is_static(self):
        return 'static' in self.access

    def __repr__(self):
        return f"<SmaliMethod {self.name}{self.signature}>"


def parse_smali_file(content):
    lines = content.split('\n')
    methods = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('.method'):
            start_line = i
            match = re.match(r'\.method\s+(.*?)\s+(\S+?)(\(.*)$', line)
            if match:
                access = match.group(1)
                name = match.group(2)
                signature = match.group(3)
                registers = 0
                is_locals = False
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith('.end method'):
                    reg_match = re.match(r'\s*\.(registers|locals)\s+(\d+)', lines[j])
                    if reg_match:
                        registers = int(reg_match.group(2))
                        is_locals = (reg_match.group(1) == 'locals')
                        break
                    j += 1
                end_line = j
                while end_line < len(lines) and not lines[end_line].strip().startswith('.end method'):
                    end_line += 1
                methods.append(SmaliMethod(name, signature, access, registers,
                                           start_line, end_line, is_locals))
                i = end_line
        i += 1
    return lines, methods


# ============================================================
# CÁLCULO DE REGISTROS SEGUROS
# ============================================================

def _type_size(desc: str) -> int:
    if desc in ('J', 'D'):
        return 2
    return 1


def count_parameter_registers(method: SmaliMethod) -> int:
    total = 0
    if not method.is_static():
        total += 1
    for p in method.parameters:
        total += _type_size(p)
    return total


def _normalize_reg(reg: str, method: SmaliMethod) -> str:
    reg = reg.strip()
    if reg.startswith('v') and reg[1:].isdigit():
        return reg
    if reg.startswith('p') and reg[1:].isdigit():
        p_index = int(reg[1:])
        n = method.registers
        n_params = count_parameter_registers(method)
        v_index = (n - n_params) + p_index
        return f"v{v_index}"
    return reg


def _param_register_set(method: SmaliMethod) -> set:
    n = method.registers
    n_params = count_parameter_registers(method)
    start = n - n_params
    return {f"v{start + i}" for i in range(n_params)}


def find_free_registers(method: SmaliMethod, return_reg=None, need=2,
                        prefer_high=False):
    n = method.registers
    n_params = count_parameter_registers(method)
    param_start = n - n_params

    forbidden = _param_register_set(method)
    if return_reg:
        forbidden.add(_normalize_reg(return_reg, method))

    candidates = [f"v{i}" for i in range(param_start)]
    if prefer_high:
        candidates.reverse()

    free = [r for r in candidates if r not in forbidden]
    if len(free) < need:
        return None
    return free[:need]


def auto_expand_registers(method: SmaliMethod, need_extra: int) -> int:
    n = method.registers
    n_params = count_parameter_registers(method)
    available = n - n_params
    if available >= need_extra:
        return n
    return n + (need_extra - available)


def plan_hook_registers(method: SmaliMethod, need=2, return_reg=None):
    temps = find_free_registers(method, return_reg=return_reg, need=need)
    if temps:
        return {
            'expand_to': None,
            'temps': temps,
            'forbidden': _param_register_set(method) | (
                {_normalize_reg(return_reg, method)} if return_reg else set()
            ),
        }

    new_n = auto_expand_registers(method, need_extra=need)
    saved = method.registers
    method.registers = new_n
    try:
        temps = find_free_registers(method, return_reg=return_reg, need=need)
    finally:
        method.registers = saved

    return {
        'expand_to': new_n,
        'temps': temps,
        'forbidden': _param_register_set(method) | (
            {_normalize_reg(return_reg, method)} if return_reg else set()
        ),
    }


# ============================================================
# GENERADORES
# ============================================================

def indent(code, spaces=4):
    prefix = ' ' * spaces
    return '\n'.join(prefix + line if line.strip() else line for line in code.split('\n'))


def generate_hook_enter(func_name, arg_name, arg_register, temps, indent_spaces=4):
    t_name, t_argname, t_val = temps[0], temps[1], temps[2]
    return indent(f"""
# ========== HOOK ENTER ==========
const-string {t_name}, "{func_name}"
const-string {t_argname}, "{arg_name}"
move-object {t_val}, {arg_register}
invoke-static {{{t_name}, {t_argname}, {t_val}}}, {REMOTE_LOGGER_CLASS}->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V
# ================================
""".strip(), indent_spaces)


def generate_hook_exit(func_name, return_reg, return_line, temps, indent_spaces=4):
    t_name, t_val = temps[0], temps[1]

    if return_line is None or return_line == 'return-void':
        return indent(f"""
# ========== HOOK EXIT (void) ==========
const-string {t_name}, "{func_name}"
const-string {t_val}, "void"
invoke-static {{{t_name}, {t_val}}}, {REMOTE_LOGGER_CLASS}->d(Ljava/lang/String;Ljava/lang/String;)V
# ======================================
""".strip(), indent_spaces)

    if return_line.startswith('return-object'):
        return indent(f"""
# ========== HOOK EXIT (object) ==========
const-string {t_name}, "{func_name}"
move-object {t_val}, {return_reg}
invoke-static {{{t_name}, {t_val}}}, {REMOTE_LOGGER_CLASS}->hookExit(Ljava/lang/String;Ljava/lang/Object;)V
# ========================================
""".strip(), indent_spaces)

    if return_line.startswith('return-wide'):
        return indent(f"""
# ========== HOOK EXIT (wide) ==========
const-string {t_name}, "{func_name}"
invoke-static {{{return_reg}}}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;
move-result-object {t_val}
invoke-static {{{t_name}, {t_val}}}, {REMOTE_LOGGER_CLASS}->hookExit(Ljava/lang/String;Ljava/lang/Object;)V
# ======================================
""".strip(), indent_spaces)

    return indent(f"""
# ========== HOOK EXIT (primitive) ==========
const-string {t_name}, "{func_name}"
invoke-static {{{return_reg}}}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;
move-result-object {t_val}
invoke-static {{{t_name}, {t_val}}}, {REMOTE_LOGGER_CLASS}->hookExit(Ljava/lang/String;Ljava/lang/Object;)V
# ===========================================
""".strip(), indent_spaces)


def generate_d_log(tag, message, temps, indent_spaces=4):
    t_tag, t_msg = temps[0], temps[1]
    return indent(f"""
# ========== LOG D ==========
const-string {t_tag}, "{tag}"
const-string {t_msg}, "{message}"
invoke-static {{{t_tag}, {t_msg}}}, {REMOTE_LOGGER_CLASS}->d(Ljava/lang/String;Ljava/lang/String;)V
# ============================
""".strip(), indent_spaces)


# ============================================================
# INJECTOR
# ============================================================

class HookInjector:
    def __init__(self, file_path, method_name):
        self.file_path = Path(file_path)
        self.method_name = method_name
        self.lines = None
        self.methods = []
        self.target_method = None
        self.pending_registers = None

    def load(self):
        if not self.file_path.exists():
            log_error(f"Archivo no encontrado: {self.file_path}")
            return False
        content = self.file_path.read_text(encoding='utf-8')
        self.lines, self.methods = parse_smali_file(content)
        for m in self.methods:
            if m.name == self.method_name:
                self.target_method = m
                break
        if not self.target_method:
            log_error(f"Método '{self.method_name}' no encontrado")
            log_info(f"Métodos disponibles: {[m.name for m in self.methods]}")
            return False
        return True

    def _find_registers_line(self):
        m = self.target_method
        for i in range(m.start_line, m.end_line):
            if re.match(r'\s*\.(registers|locals)\s+\d+', self.lines[i]):
                return i
        return None

    def _find_end_method_line(self):
        for i in range(self.target_method.start_line, len(self.lines)):
            if self.lines[i].strip().startswith('.end method'):
                return i
        return None

    def _apply_register_plan(self, plan):
        if plan['expand_to'] is not None:
            self.pending_registers = plan['expand_to']
            log_info(f"Registros se expandirán a: {plan['expand_to']}")

    def _write_registers_to_lines(self):
        if self.pending_registers is None:
            return
        idx = self._find_registers_line()
        if idx is None:
            return
        old = self.target_method.registers
        self.lines[idx] = re.sub(
            r'(\.(registers|locals)\s+)\d+',
            f'\\g<1>{self.pending_registers}',
            self.lines[idx]
        )
        self.target_method.registers = self.pending_registers
        log_info(f"Registros aplicados: {old} → {self.pending_registers}")

    def inject_enter(self):
        m = self.target_method
        if m.is_static():
            if not m.parameters:
                log_warn("Método static sin parámetros: hook enter sin valor")
                arg_register = None
            else:
                arg_register = _normalize_reg("p0", m)
        else:
            arg_register = _normalize_reg("p0", m)

        plan = plan_hook_registers(m, need=3, return_reg=arg_register)
        self._apply_register_plan(plan)
        temps = plan['temps']

        reg_line_idx = self._find_registers_line()
        if reg_line_idx is None:
            log_error("No se encontró .registers/.locals")
            return False

        hook_code = generate_hook_enter(
            func_name=m.name,
            arg_name="this" if not m.is_static() else "arg0",
            arg_register=arg_register if arg_register else "v0",
            temps=temps,
        )

        self.lines.insert(reg_line_idx + 1, "")
        self.lines.insert(reg_line_idx + 1, f"    # Hook ENTER inyectado - {datetime.now().isoformat()}")
        self.lines.insert(reg_line_idx + 1, hook_code)

        log_ok(f"Hook ENTER inyectado en {m.name} usando {temps}")
        return True

    def inject_exit(self):
        m = self.target_method
        end_idx = self._find_end_method_line()
        if end_idx is None:
            log_error("No se encontró .end method")
            return False

        return_indices = [
            i for i in range(m.start_line, end_idx)
            if self.lines[i].strip().startswith('return-')
        ]
        if not return_indices:
            log_warn(f"No se encontraron returns en {m.name}")
            return False

        first_line = self.lines[return_indices[0]].strip()
        first_reg_match = re.search(r'return-\S+\s+(\S+)', first_line)
        first_reg = first_reg_match.group(1) if first_reg_match else None

        plan = plan_hook_registers(m, need=2, return_reg=first_reg)
        self._apply_register_plan(plan)
        temps = plan['temps']

        for idx in reversed(return_indices):
            line = self.lines[idx].strip()

            if line == 'return-void':
                hook_code = generate_hook_exit(m.name, None, line, temps)
                self.lines.insert(idx, "")
                self.lines.insert(idx, hook_code)
                continue

            match = re.search(r'return-(\S+)\s+(\S+)', line)
            if not match:
                continue
            kind = match.group(1)
            reg = match.group(2)

            reg_norm = _normalize_reg(reg, m)

            if reg_norm in temps:
                plan3 = plan_hook_registers(m, need=3, return_reg=reg_norm)
                self._apply_register_plan(plan3)
                extra = plan3['temps'][2]
                if kind == 'object':
                    self.lines.insert(idx, f"    move-object {extra}, {reg}")
                elif kind == 'wide':
                    self.lines.insert(idx, f"    move-wide {extra}, {reg}")
                else:
                    self.lines.insert(idx, f"    move {extra}, {reg}")
                reg_norm = extra

            hook_code = generate_hook_exit(m.name, reg_norm, line, temps)
            self.lines.insert(idx, "")
            self.lines.insert(idx, hook_code)

        log_ok(f"Hook EXIT inyectado en {m.name} ({len(return_indices)} returns) "
               f"usando {temps}")
        return True

    def inject_d(self, tag, message):
        m = self.target_method
        plan = plan_hook_registers(m, need=2, return_reg=None)
        self._apply_register_plan(plan)
        temps = plan['temps']

        reg_line_idx = self._find_registers_line()
        if reg_line_idx is None:
            log_error("No se encontró .registers/.locals")
            return False

        log_code = generate_d_log(tag, message, temps)
        self.lines.insert(reg_line_idx + 1, "")
        self.lines.insert(reg_line_idx + 1, f"    # Log D inyectado - {datetime.now().isoformat()}")
        self.lines.insert(reg_line_idx + 1, log_code)

        log_ok(f'Log d("{tag}", "{message}") inyectado en {m.name} usando {temps}')
        return True

    def save(self, backup=True):
        self._write_registers_to_lines()

        if backup:
            backup_path = self.file_path.with_suffix('.smali.bak')
            shutil.copy2(self.file_path, backup_path)
            log_info(f"Backup guardado en: {backup_path}")
        self.file_path.write_text('\n'.join(self.lines), encoding='utf-8')
        log_ok(f"Archivo guardado: {self.file_path}")


# ============================================================
# ANALYZE
# ============================================================

def analyze_method(method: SmaliMethod):
    log_header(f"Método: {method.name}")
    print(f"  {Color.CYAN}Signature:{Color.RESET} {method.signature}")
    print(f"  {Color.CYAN}Access:{Color.RESET}    {method.access}")
    directive = ".locals" if method.is_locals else ".registers"
    print(f"  {Color.CYAN}Directiva:{Color.RESET} {directive} {method.registers}")
    print(f"  {Color.CYAN}Static:{Color.RESET}    {method.is_static()}")
    print(f"  {Color.CYAN}Return:{Color.RESET}    {method.return_type}")

    n_params = count_parameter_registers(method)
    param_start = method.registers - n_params
    print(f"  {Color.CYAN}Params en registros:{Color.RESET} {n_params} "
          f"(p0 → v{param_start})")

    if method.parameters:
        print(f"  {Color.CYAN}Parámetros:{Color.RESET}")
        for i, p in enumerate(method.parameters):
            size = _type_size(p)
            print(f"    p{i} : {p}  ({size} reg)")

    free = find_free_registers(method, need=1)
    if free is None:
        print(f"  {Color.YELLOW}No hay registros no-param libres.{Color.RESET}")
    else:
        libres = [f"v{i}" for i in range(param_start)
                  if f"v{i}" not in _param_register_set(method)]
        print(f"  {Color.CYAN}Registros no-param:{Color.RESET} {libres}")

    print()


# ============================================================
# PARSER PROPIO (reutilizable)
# ============================================================

def build_hook_parser(prog: str = "smalilog hook") -> argparse.ArgumentParser:
    """Construye el parser del subcomando `hook`."""
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Inyecta hooks de observación en archivos Smali",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  smalilog hook archivo.smali --list
  smalilog hook archivo.smali --method Sf --analyze
  smalilog hook archivo.smali --method Sf --action enter
  smalilog hook archivo.smali --method Sf --action exit
  smalilog hook archivo.smali --method Sf --action both
  smalilog hook archivo.smali --method Sf --action d --tag MiTag --message "Hola"
        """,
    )

    parser.add_argument('file', help='Archivo Smali a procesar')
    parser.add_argument('--method', '-m', help='Nombre del método objetivo', default=None)
    parser.add_argument(
        '--action', '-a',
        choices=['enter', 'exit', 'both', 'observ', 'analyze', 'd'],
        default='both',
        help='Acción: enter, exit, both, observ, analyze, d (default: both)',
    )
    parser.add_argument('--tag', help='Tag para acción "d" (default: LOG)', default='LOG')
    parser.add_argument('--message', '--msg', help='Mensaje para acción "d"',
                        default='Mensaje de log')
    parser.add_argument('--analyze', action='store_true', help='Solo analizar')
    parser.add_argument('--list', '-l', action='store_true', help='Listar métodos')
    parser.add_argument('--no-backup', action='store_true', help='No crear backup')
    parser.add_argument('--output', '-o', help='Archivo de salida')

    return parser


def run_hooker(argv: list[str] | None = None, prog: str = "smalilog hook") -> int:
    """
    Ejecuta el inyector. Devuelve 0 en éxito, != 0 en error.
    Se puede llamar desde tests o desde el CLI principal.
    """
    parser = build_hook_parser(prog=prog)
    args = parser.parse_args(argv)

    log_header("smalilog hook - Inyector de hooks")

    injector = HookInjector(args.file, args.method)
    if not injector.load():
        return 1

    if args.list:
        log_header(f"Métodos en {args.file}")
        for m in injector.methods:
            static = "static " if m.is_static() else ""
            print(f"  {Color.GREEN}{m.name}{Color.RESET} {m.signature} "
                  f"({static}{m.registers} regs)")
        return 0

    if args.analyze or args.action == 'analyze':
        analyze_method(injector.target_method)
        return 0

    if not args.method:
        log_error("Debes especificar --method")
        return 1

    log_info(f"Archivo: {args.file}")
    log_info(f"Método: {args.method}")
    log_info(f"Acción: {args.action}")

    analyze_method(injector.target_method)

    success = False

    if args.action == 'd':
        success = injector.inject_d(args.tag, args.message)
    elif args.action == 'enter':
        success = injector.inject_enter()
    elif args.action == 'exit':
        success = injector.inject_exit()
    elif args.action in ('both', 'observ'):
        if injector.inject_enter():
            success = True
        if injector.inject_exit():
            success = True

    if success:
        output_path = args.output if args.output else args.file
        injector.file_path = Path(output_path)
        injector.save(backup=not args.no_backup)
        log_header("INYECCIÓN COMPLETADA")
        return 0
    else:
        log_error("No se pudo completar la inyección")
        return 1


# Compatibilidad: permite `python -m smalilog.injector.hooker ...`
if __name__ == '__main__':
    sys.exit(run_hooker())
