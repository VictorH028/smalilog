#!/usr/bin/env python3
"""
smali_hook.py - Inyecta hooks de observación en archivos Smali

Uso:
    python3 smali_hook.py archivo.smali --method metodo --action observ
    python3 smali_hook.py archivo.smali --method metodo --action enter
    python3 smali_hook.py archivo.smali --method metodo --action exit
    python3 smali_hook.py archivo.smali --method metodo --action both
    python3 smali_hook.py archivo.smali --method metodo --action d --tag MiTag --message "Hola"
"""

import argparse
import re
import sys
import shutil
from pathlib import Path
from datetime import datetime

# ============================================================
# CONFIGURACIÓN
# ============================================================

REMOTE_LOGGER_CLASS = "Lcom/deadnote/RemoteLogger;"
EXTRA_REGISTERS = 4

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

def log_info(msg):    print(f"{Color.BLUE}[INFO]{Color.RESET} {msg}")
def log_ok(msg):      print(f"{Color.GREEN}[OK]{Color.RESET} {msg}")
def log_warn(msg):    print(f"{Color.YELLOW}[WARN]{Color.RESET} {msg}")
def log_error(msg):   print(f"{Color.RED}[ERROR]{Color.RESET} {msg}")
def log_header(msg):
    print(f"\n{Color.BOLD}{Color.CYAN}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN}{msg}{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN}{'='*60}{Color.RESET}\n")

# ============================================================
# PARSER
# ============================================================

class SmaliMethod:
    def __init__(self, name, signature, access, registers, start_line, end_line):
        self.name = name
        self.signature = signature
        self.access = access
        self.registers = registers
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
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith('.end method'):
                    reg_match = re.match(r'\s*\.(registers|locals)\s+(\d+)', lines[j])
                    if reg_match:
                        registers = int(reg_match.group(2))
                        break
                    j += 1
                end_line = j
                while end_line < len(lines) and not lines[end_line].strip().startswith('.end method'):
                    end_line += 1
                methods.append(SmaliMethod(name, signature, access, registers, start_line, end_line))
                i = end_line
        i += 1
    return lines, methods


# ============================================================
# GENERADORES
# ============================================================

def indent(code, spaces=4):
    prefix = ' ' * spaces
    return '\n'.join(prefix + line if line.strip() else line for line in code.split('\n'))


def generate_hook_enter(func_name, arg_name, arg_register, indent_spaces=4):
    return indent(f"""
# ========== HOOK ENTER ==========
const-string v0, "{func_name}"
const-string v1, "{arg_name}"
move-object v2, {arg_register}
invoke-static {{v0, v1, v2}}, {REMOTE_LOGGER_CLASS}->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V
# ================================
""".strip(), indent_spaces)


def generate_hook_exit(func_name, result_register=None, return_line=None, indent_spaces=4):
    if return_line is None or return_line == 'return-void':
        code = f"""
# ========== HOOK EXIT ==========
const-string v0, "{func_name}"
const-string v1, "void"
invoke-static {{v0, v1}}, {REMOTE_LOGGER_CLASS}->d(Ljava/lang/String;Ljava/lang/String;)V
# ================================
"""
    elif return_line.startswith('return-object'):
        code = f"""
# ========== HOOK EXIT ==========
const-string v0, "{func_name}"
move-object v1, {result_register}
invoke-static {{v0, v1}}, {REMOTE_LOGGER_CLASS}->hookExit(Ljava/lang/String;Ljava/lang/Object;)V
# ================================
"""
    elif return_line.startswith('return-wide'):
        code = f"""
# ========== HOOK EXIT ==========
const-string v0, "{func_name}"
invoke-static {{{result_register}}}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;
move-result-object v1
invoke-static {{v0, v1}}, {REMOTE_LOGGER_CLASS}->hookExit(Ljava/lang/String;Ljava/lang/Object;)V
# ================================
"""
    else:
        code = f"""
# ========== HOOK EXIT ==========
const-string v0, "{func_name}"
invoke-static {{{result_register}}}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;
move-result-object v1
invoke-static {{v0, v1}}, {REMOTE_LOGGER_CLASS}->hookExit(Ljava/lang/String;Ljava/lang/Object;)V
# ================================
"""
    return indent(code.strip(), indent_spaces)


def generate_d_log(tag, message, indent_spaces=4):
    return indent(f"""
# ========== LOG D ==========
const-string v0, "{tag}"
const-string v1, "{message}"
invoke-static {{v0, v1}}, {REMOTE_LOGGER_CLASS}->d(Ljava/lang/String;Ljava/lang/String;)V
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
    
    def inject_enter(self):
        m = self.target_method
        reg_line_idx = self._find_registers_line()
        if reg_line_idx is None:
            log_error("No se encontró .registers/.locals")
            return False
        
        hook_code = generate_hook_enter(
            func_name=m.name,
            arg_name="this" if not m.is_static() else (m.parameters[0] if m.parameters else "no_args"),
            arg_register="p0",
        )
        
        self.lines.insert(reg_line_idx + 1, hook_code)
        self.lines.insert(reg_line_idx + 1, "")
        self.lines.insert(reg_line_idx + 1, f"    # Hook ENTER inyectado - {datetime.now().isoformat()}")
        
        log_ok(f"Hook ENTER inyectado en {m.name}")
        return True
    
    def inject_exit(self):
        m = self.target_method
        end_idx = self._find_end_method_line()
        if end_idx is None:
            log_error("No se encontró .end method")
            return False
        
        return_indices = []
        for i in range(m.start_line, end_idx):
            line = self.lines[i].strip()
            if line.startswith('return-'):
                return_indices.append(i)
        
        if not return_indices:
            log_warn(f"No se encontraron returns en {m.name}")
            return False
        
        for idx in reversed(return_indices):
            line = self.lines[idx].strip()
            if line == 'return-void':
                hook_code = generate_hook_exit(m.name, None, line)
            else:
                match = re.search(r'return-\S+\s+(\S+)', line)
                result_reg = match.group(1) if match else None
                hook_code = generate_hook_exit(m.name, result_reg, line)
            
            self.lines.insert(idx, "")
            self.lines.insert(idx, hook_code)
        
        log_ok(f"Hook EXIT inyectado en {m.name} ({len(return_indices)} returns)")
        return True
    
    def inject_d(self, tag, message):
        m = self.target_method
        reg_line_idx = self._find_registers_line()
        if reg_line_idx is None:
            log_error("No se encontró .registers/.locals")
            return False
        
        log_code = generate_d_log(tag, message)
        self.lines.insert(reg_line_idx + 1, log_code)
        self.lines.insert(reg_line_idx + 1, "")
        self.lines.insert(reg_line_idx + 1, f"    # Log D inyectado - {datetime.now().isoformat()}")
        
        log_ok(f"Log d(\"{tag}\", \"{message}\") inyectado en {m.name}")
        return True
    
    def increase_registers(self):
        m = self.target_method
        for i in range(m.start_line, min(m.start_line + 20, len(self.lines))):
            match = re.match(r'(\s*\.(registers|locals)\s+)(\d+)', self.lines[i])
            if match:
                old_regs = int(match.group(3))
                new_regs = old_regs + EXTRA_REGISTERS
                self.lines[i] = re.sub(r'(\.(registers|locals)\s+)\d+', f'\\g<1>{new_regs}', self.lines[i])
                log_info(f"Registros aumentados: {old_regs} → {new_regs}")
                return True
        log_error("No se pudo aumentar registros")
        return False
    
    def save(self, backup=True):
        if backup:
            backup_path = self.file_path.with_suffix('.smali.bak')
            shutil.copy2(self.file_path, backup_path)
            log_info(f"Backup guardado en: {backup_path}")
        self.file_path.write_text('\n'.join(self.lines), encoding='utf-8')
        log_ok(f"Archivo guardado: {self.file_path}")


# ============================================================
# ANALYZE
# ============================================================

def analyze_method(method):
    log_header(f"Método: {method.name}")
    print(f"  {Color.CYAN}Signature:{Color.RESET} {method.signature}")
    print(f"  {Color.CYAN}Access:{Color.RESET}    {method.access}")
    print(f"  {Color.CYAN}Registers:{Color.RESET} {method.registers}")
    print(f"  {Color.CYAN}Static:{Color.RESET}    {method.is_static()}")
    print(f"  {Color.CYAN}Return:{Color.RESET}    {method.return_type}")
    if method.parameters:
        print(f"  {Color.CYAN}Parámetros:{Color.RESET}")
        for i, p in enumerate(method.parameters):
            print(f"    p{i} : {p}")
    print(f"  {Color.CYAN}Registros recomendados:{Color.RESET} {method.registers + EXTRA_REGISTERS}")
    print()


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Inyecta hooks de observación en archivos Smali",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python3 smali_hook.py archivo.smali --list
  python3 smali_hook.py archivo.smali --method Sf --analyze
  python3 smali_hook.py archivo.smali --method Sf --action enter
  python3 smali_hook.py archivo.smali --method Sf --action exit
  python3 smali_hook.py archivo.smali --method Sf --action both
  python3 smali_hook.py archivo.smali --method Sf --action d --tag MiTag --message "Hola"
  python3 smali_hook.py archivo.smali --method Sf --action both --auto-registers
        """
    )
    
    parser.add_argument('file', help='Archivo Smali a procesar')
    parser.add_argument('--method', '-m', help='Nombre del método objetivo', default=None)
    parser.add_argument(
        '--action', '-a',
        choices=['enter', 'exit', 'both', 'observ', 'analyze', 'd'],
        default='both',
        help='Acción: enter, exit, both, observ, analyze, d (default: both)'
    )
    parser.add_argument('--tag', help='Tag para acción "d" (default: LOG)', default='LOG')
    parser.add_argument('--message', '--msg', help='Mensaje para acción "d"', default='Mensaje de log')
    parser.add_argument('--analyze', action='store_true', help='Solo analizar')
    parser.add_argument('--list', '-l', action='store_true', help='Listar métodos')
    parser.add_argument('--auto-registers', action='store_true', help='Aumentar registros automáticamente')
    parser.add_argument('--no-backup', action='store_true', help='No crear backup')
    parser.add_argument('--output', '-o', help='Archivo de salida')
    
    args = parser.parse_args()
    
    log_header("smali_hook.py - Inyector de hooks")
    
    injector = HookInjector(args.file, args.method)
    if not injector.load():
        sys.exit(1)
    
    if args.list:
        log_header(f"Métodos en {args.file}")
        for m in injector.methods:
            static = "static " if m.is_static() else ""
            print(f"  {Color.GREEN}{m.name}{Color.RESET} {m.signature} ({static}{m.registers} regs)")
        return
    
    if args.analyze or args.action == 'analyze':
        analyze_method(injector.target_method)
        return
    
    if not args.method:
        log_error("Debes especificar --method")
        sys.exit(1)
    
    log_info(f"Archivo: {args.file}")
    log_info(f"Método: {args.method}")
    log_info(f"Acción: {args.action}")
    
    analyze_method(injector.target_method)
    
    if args.auto_registers or args.action in ('enter', 'exit', 'both', 'observ', 'd'):
        injector.increase_registers()
    
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
        log_header("✅ INYECCIÓN COMPLETADA")
    else:
        log_error("No se pudo completar la inyección")
        sys.exit(1)


if __name__ == '__main__':
    main()
