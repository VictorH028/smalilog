#!/usr/bin/env python3
"""
smali_hook.py - Inyecta hooks de observación en archivos Smali

Uso:
    python3 smali_hook.py archivo.smali --method metodo --action observ
    python3 smali_hook.py archivo.smali --method metodo --action enter
    python3 smali_hook.py archivo.smali --method metodo --action exit
    python3 smali_hook.py archivo.smali --method metodo --action both
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

# Cuántos registros extra añadir para los hooks
EXTRA_REGISTERS = 4

# ============================================================
# COLORES PARA TERMINAL
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
def log_header(msg):  print(f"\n{Color.BOLD}{Color.CYAN}{'='*60}{Color.RESET}")
def log_header(msg):  print(f"{Color.BOLD}{Color.CYAN}{msg}{Color.RESET}")
def log_header(msg):  print(f"{Color.BOLD}{Color.CYAN}{'='*60}{Color.RESET}\n")

# ============================================================
# PARSER DE SMALI
# ============================================================

class SmaliMethod:
    """Representa un método Smali"""
    
    def __init__(self, name, signature, access, registers, body_lines, start_line, end_line):
        self.name = name
        self.signature = signature
        self.access = access
        self.registers = registers
        self.body_lines = body_lines
        self.start_line = start_line
        self.end_line = end_line
        self.parameters = self._parse_parameters()
        self.return_type = self._parse_return_type()
    
    def _parse_parameters(self):
        """Extrae los parámetros del signature"""
        # Signature ejemplo: (Lcom/example/Activity;Ljava/lang/String;I)V
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
                while params_str[i] == '[':
                    i += 1
                if params_str[i] == 'L':
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
        """Extrae el tipo de retorno"""
        match = re.search(r'\)(.+)$', self.signature)
        return match.group(1) if match else 'V'
    
    def is_static(self):
        return 'static' in self.access
    
    def get_param_register(self, index):
        """
        Calcula el registro pX para un parámetro.
        Los parámetros son p0, p1, p2... desde el final.
        
        Para métodos NO estáticos: p0 = this, p1 = primer arg
        Para métodos static: p0 = primer arg
        """
        offset = 0 if self.is_static() else 1
        # Los parámetros de 64 bits (J, D) ocupan 2 registros
        reg_offset = 0
        for i in range(index):
            param = self.parameters[i]
            if param in ('J', 'D'):  # long, double
                reg_offset += 2
            else:
                reg_offset += 1
        
        return f"p{index + offset + (reg_offset - index)}" if reg_offset > index else f"p{index + offset}"
    
    def __repr__(self):
        return f"<SmaliMethod {self.name}{self.signature}>"


def parse_smali_file(content):
    """Parsea un archivo Smali y devuelve las líneas y métodos"""
    lines = content.split('\n')
    methods = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('.method'):
            start_line = i
            # Extraer access, name, signature
            # .method public static final Rf(Lcom/.../UpgradeActivity;)Lmt/b;
            match = re.match(r'\.method\s+(.*?)\s+(\S+?)(\(.*)$', line)
            if match:
                access = match.group(1)
                name = match.group(2)
                signature = match.group(3)
                
                # Buscar .registers o .locals
                registers = 0
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith('.end method'):
                    reg_line = lines[j].strip()
                    reg_match = re.match(r'\.(registers|locals)\s+(\d+)', reg_line)
                    if reg_match:
                        registers = int(reg_match.group(2))
                        break
                    j += 1
                
                # Encontrar .end method
                end_line = j
                while end_line < len(lines) and not lines[end_line].strip().startswith('.end method'):
                    end_line += 1
                
                body_lines = lines[start_line:end_line+1]
                
                methods.append(SmaliMethod(
                    name=name,
                    signature=signature,
                    access=access,
                    registers=registers,
                    body_lines=body_lines,
                    start_line=start_line,
                    end_line=end_line
                ))
                
                i = end_line
        
        i += 1
    
    return lines, methods


# ============================================================
# GENERADORES DE CÓDIGO SMALI
# ============================================================

def indent(code, spaces=4):
    """Indenta un bloque de código"""
    prefix = ' ' * spaces
    return '\n'.join(prefix + line if line.strip() else line for line in code.split('\n'))


def generate_hook_enter(func_name, arg_name, arg_register, indent_spaces=4):
    """Genera código Smali para hookEnter"""
    return indent(f"""
# ========== HOOK ENTER ==========
const-string v0, "{func_name}"
const-string v1, "{arg_name}"
move-object v2, {arg_register}
invoke-static {{v0, v1, v2}}, {REMOTE_LOGGER_CLASS}->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V
# ================================
""".strip(), indent_spaces)


def generate_hook_exit(func_name, result_register=None, indent_spaces=4):
    """Genera código Smali para hookExit"""
    if result_register is None:
        # Sin resultado, solo log
        code = f"""
# ========== HOOK EXIT ==========
const-string v0, "{func_name}"
const-string v1, "void"
invoke-static {{v0, v1}}, {REMOTE_LOGGER_CLASS}->d(Ljava/lang/String;Ljava/lang/String;)V
# ================================
"""
    else:
        # Convertir a Object si es primitivo
        code = f"""
# ========== HOOK EXIT ==========
const-string v0, "{func_name}"
move-object v1, {result_register}
invoke-static {{v0, v1}}, {REMOTE_LOGGER_CLASS}->hookExit(Ljava/lang/String;Ljava/lang/Object;)V
# ================================
"""
    return indent(code.strip(), indent_spaces)


def generate_simple_log(tag, message, indent_spaces=4):
    """Genera un log simple"""
    return indent(f"""
const-string v0, "{tag}"
const-string v1, "{message}"
invoke-static {{v0, v1}}, {REMOTE_LOGGER_CLASS}->d(Ljava/lang/String;Ljava/lang/String;)V
""".strip(), indent_spaces)


# ============================================================
# INYECTOR DE HOOKS
# ============================================================

class HookInjector:
    def __init__(self, file_path, method_name):
        self.file_path = Path(file_path)
        self.method_name = method_name
        self.content = None
        self.lines = None
        self.methods = []
        self.target_method = None
        self.modified_lines = None
    
    def load(self):
        """Carga y parsea el archivo"""
        if not self.file_path.exists():
            log_error(f"Archivo no encontrado: {self.file_path}")
            return False
        
        self.content = self.file_path.read_text(encoding='utf-8')
        self.lines, self.methods = parse_smali_file(self.content)
        
        # Buscar el método objetivo
        for m in self.methods:
            if m.name == self.method_name:
                self.target_method = m
                break
        
        if not self.target_method:
            log_error(f"Método '{self.method_name}' no encontrado")
            log_info(f"Métodos disponibles: {[m.name for m in self.methods]}")
            return False
        
        return True
    
    def find_target_method(self):
        """Encuentra el método objetivo"""
        for m in self.methods:
            if m.name == self.method_name:
                return m
        return None
   
    def inject_d(self, tag, message):
     """Inyecta un log simple d(tag, message) al inicio del método"""
        m = self.target_method
    
        # Encontrar la línea de .registers/.locals
        reg_line_idx = None
        for i in range(m.start_line, m.end_line):
            if re.match(r'\s*\.(registers|locals)\s+\d+', self.lines[i]):
                reg_line_idx = i
                break
    
        if reg_line_idx is None:
            log_error("No se encontró .registers/.locals")
            return False
    
        # Construir el log
        log_code = indent(f"""
        # ========== LOG D ==========
        const-string v0, "{tag}"
        const-string v1, "{message}"
        invoke-static {{v0, v1}}, {REMOTE_LOGGER_CLASS}->d(Ljava/lang/String;Ljava/lang/String;)V
        # ============================
        """.strip())
    
       # Insertar después de .registers
        self.lines.insert(reg_line_idx + 1, log_code)
        self.lines.insert(reg_line_idx + 1, "")
        self.lines.insert(reg_line_idx + 1, f"    # Log inyectado por smali_hook.py - {datetime.now().isoformat()}")
    
        log_ok(f"Log d(\"{tag}\", \"{message}\") inyectado en {m.name}")
        return True

    def inject_enter(self):
        """Inyecta hook ENTER al inicio del método"""
        m = self.target_method
        
        # Encontrar la línea de .registers/.locals
        reg_line_idx = None
        for i in range(m.start_line, m.end_line):
            if re.match(r'\s*\.(registers|locals)\s+\d+', self.lines[i]):
                reg_line_idx = i
                break
        
        if reg_line_idx is None:
            log_error("No se encontró .registers/.locals")
            return False
        
        # Construir el hook
        hook_code = generate_hook_enter(
            func_name=m.name,
            arg_name="this" if not m.is_static() else m.parameters[0] if m.parameters else "no_args",
            arg_register="p0" if not m.is_static() else "p0",
        )
        
        # Insertar después de .registers
        self.lines.insert(reg_line_idx + 1, hook_code)
        self.lines.insert(reg_line_idx + 1, "")  # Línea en blanco
        self.lines.insert(reg_line_idx + 1, f"    # Hook inyectado por smali_hook.py - {datetime.now().isoformat()}")
        
        log_ok(f"Hook ENTER inyectado en {m.name}")
        return True
    
    def inject_exit(self):
        """Inyecta hook EXIT antes de cada return"""
        m = self.target_method
        
        # Re-calcular posiciones porque las líneas pueden haber cambiado
        # Buscar el final del método
        end_idx = m.end_line
        for i in range(m.start_line, len(self.lines)):
            if self.lines[i].strip().startswith('.end method'):
                end_idx = i
                break
        
        # Buscar todos los returns
        return_indices = []
        for i in range(m.start_line, end_idx):
            line = self.lines[i].strip()
            if line.startswith('return-'):
                return_indices.append(i)
        
        if not return_indices:
            log_warn(f"No se encontraron returns en {m.name}")
            return False
        
        # Inyectar antes de cada return (de abajo hacia arriba para no descolocar índices)
        return_type = m.return_type
        
        for idx in reversed(return_indices):
            line = self.lines[idx].strip()
            
            # Determinar el registro del resultado
            if line == 'return-void':
                result_reg = None
                hook_code = generate_hook_exit(m.name, None)
            else:
                # return-object vX o return vX (primitivo)
                match = re.search(r'return-\S+\s+(\S+)', line)
                if match:
                    result_reg = match.group(1)
                    # Si es primitivo, hay que convertirlo a Object
                    if line.startswith('return-object'):
                        hook_code = generate_hook_exit(m.name, result_reg)
                    else:
                        # Convertir primitivo a Object usando valueOf
                        hook_code = generate_exit_with_boxing(m.name, result_reg, line)
                else:
                    hook_code = generate_hook_exit(m.name, None)
            
            self.lines.insert(idx, "")
            self.lines.insert(idx, hook_code)
        
        log_ok(f"Hook EXIT inyectado en {m.name} ({len(return_indices)} returns)")
        return True
    
    def increase_registers(self):
        """Aumenta el número de registros del método"""
        m = self.target_method
        
        # Re-calcular posiciones
        for i in range(m.start_line, min(m.start_line + 20, len(self.lines))):
            match = re.match(r'(\s*\.(registers|locals)\s+)(\d+)', self.lines[i])
            if match:
                old_regs = int(match.group(3))
                new_regs = old_regs + EXTRA_REGISTERS
                self.lines[i] = re.sub(
                    r'(\.(registers|locals)\s+)\d+',
                    f'\\g<1>{new_regs}',
                    self.lines[i]
                )
                log_info(f"Registros aumentados: {old_regs} → {new_regs}")
                return True
        
        log_error("No se pudo aumentar registros")
        return False
    
    def save(self, backup=True):
        """Guarda los cambios"""
        if backup:
            backup_path = self.file_path.with_suffix('.smali.bak')
            shutil.copy2(self.file_path, backup_path)
            log_info(f"Backup guardado en: {backup_path}")
        
        self.file_path.write_text('\n'.join(self.lines), encoding='utf-8')
        log_ok(f"Archivo guardado: {self.file_path}")


def generate_exit_with_boxing(func_name, result_reg, return_line):
    """Genera hook exit convirtiendo primitivos a Object"""
    # Determinar el tipo de primitivo
    if return_line.startswith('return-wide'):
        boxed = f"invoke-static {{{result_reg}}}, Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;"
        boxed += "\nmove-result-object v3"
    elif return_line.startswith('return '):
        # Puede ser int, float, boolean, etc.
        boxed = f"invoke-static {{{result_reg}}}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;"
        boxed += "\nmove-result-object v3"
    else:
        boxed = ""
    
    return indent(f"""
# ========== HOOK EXIT ==========
const-string v0, "{func_name}"
{boxed}
move-object v1, v3
invoke-static {{v0, v1}}, {REMOTE_LOGGER_CLASS}->hookExit(Ljava/lang/String;Ljava/lang/Object;)V
# ================================
""".strip())


# ============================================================
# ANÁLISIS DE MÉTODO
# ============================================================

def analyze_method(method):
    """Muestra información del método"""
    log_header(f"Método: {method.name}")
    print(f"  {Color.CYAN}Signature:{Color.RESET} {method.signature}")
    print(f"  {Color.CYAN}Access:{Color.RESET}    {method.access}")
    print(f"  {Color.CYAN}Registers:{Color.RESET} {method.registers}")
    print(f"  {Color.CYAN}Static:{Color.RESET}    {method.is_static()}")
    print(f"  {Color.CYAN}Return:{Color.RESET}    {method.return_type}")
    
    if method.parameters:
        print(f"  {Color.CYAN}Parámetros:{Color.RESET}")
        offset = 0 if method.is_static() else 1
        reg_idx = 0
        for i, p in enumerate(method.parameters):
            reg_name = f"p{i + offset}"
            print(f"    {reg_name} : {p}")
    else:
        print(f"  {Color.CYAN}Parámetros:{Color.RESET} (ninguno)")
    
    print()
    print(f"  {Color.CYAN}Tipo de retorno:{Color.RESET}")
    
    ret_type = method.return_type
    if ret_type == 'V':
        print(f"    void (no devuelve nada)")
    elif ret_type == 'Z':
        print(f"    boolean")
    elif ret_type == 'I':
        print(f"    int")
    elif ret_type == 'J':
        print(f"    long")
    elif ret_type == 'F':
        print(f"    float")
    elif ret_type == 'D':
        print(f"    double")
    elif ret_type.startswith('L'):
        class_name = ret_type[1:-1].replace('/', '.')
        print(f"    Object: {class_name}")
    elif ret_type.startswith('['):
        print(f"    Array: {ret_type}")
    else:
        print(f"    {ret_type}")
    
    print()
    print(f"  {Color.CYAN}Registros necesarios para hook:{Color.RESET}")
    print(f"    Actuales: {method.registers}")
    print(f"    Recomendados: {method.registers + EXTRA_REGISTERS}")


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Inyecta hooks de observación en archivos Smali",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Analizar un método (sin modificar)
  python3 smali_hook.py archivo.smali --method Sf --analyze
  
  # Inyectar hook ENTER
  python3 smali_hook.py archivo.smali --method Sf --action enter
  
  # Inyectar hook EXIT
  python3 smali_hook.py archivo.smali --method Sf --action exit
  
  # Inyectar ambos hooks
  python3 smali_hook.py archivo.smali --method Sf --action both
  
  # Inyectar ambos y aumentar registros automáticamente
  python3 smali_hook.py archivo.smali --method Sf --action both --auto-registers
  
  # Listar todos los métodos
  python3 smali_hook.py archivo.smali --list
        """
    )
    
    parser.add_argument(
        'file',
        help='Archivo Smali a procesar'
    )
    
    parser.add_argument(
        '--method', '-m',
        help='Nombre del método objetivo',
        default=None
    )
    
    parser.add_argument(
    '--action', '-a',
    choices=['enter', 'exit', 'both', 'observ', 'analyze', 'd'],
    default='both',
    help='Acción a realizar (default: both). "d" = log simple'
    )

    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Solo analizar el método sin modificar'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='Listar todos los métodos del archivo'
    )
    
    parser.add_argument(
        '--auto-registers',
        action='store_true',
        help='Aumentar registros automáticamente'
    )
    
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='No crear backup'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Archivo de salida (default: sobrescribir entrada)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar información detallada'
    )
    
    parser.add_argument(
    '--tag',
    help='Tag para la acción "d" (ej: MainActivity)',
    default='LOG'
    )

    parser.add_argument(
    '--message', '--msg',
    help='Mensaje para la acción "d"',
    default='Mensaje de log'
    )

    args = parser.parse_args()
    
    # ============================================================
    # EJECUTAR
    # ============================================================
    
    log_header("smali_hook.py - Inyector de hooks")
    
    injector = HookInjector(args.file, args.method)
    
    if not injector.load():
        sys.exit(1)
    
    # Listar métodos
    if args.list:
        log_header(f"Métodos en {args.file}")
        for m in injector.methods:
            static = "static " if m.is_static() else ""
            print(f"  {Color.GREEN}{m.name}{Color.RESET} {m.signature} ({static}{m.registers} regs)")
        return
    
    # Analizar
    if args.analyze or args.action == 'analyze':
        analyze_method(injector.target_method)
        return
    
    # Verificar que hay método objetivo
    if not args.method:
        log_error("Debes especificar --method")
        sys.exit(1)
    
    log_info(f"Archivo: {args.file}")
    log_info(f"Método: {args.method}")
    log_info(f"Acción: {args.action}")
    
    analyze_method(injector.target_method)
    
    # Aumentar registros si es necesario
    if args.auto_registers or args.action in ('enter', 'exit', 'both', 'observ'):
        if not injector.increase_registers():
            log_warn("Continuando sin aumentar registros (puede fallar)")
    
    # Aplicar acciones
    success = False
    
    if args.action in ('enter', 'both', 'observ'):
        if injector.inject_enter():
            success = True
    
    if args.action in ('exit', 'both', 'observ'):
        if injector.inject_exit():
            success = True
    
    if success:
        output_path = args.output if args.output else args.file
        injector.file_path = Path(output_path)
        injector.save(backup=not args.no_backup)
        
        log_header("✅ INYECCIÓN COMPLETADA")
        log_info(f"Archivo modificado: {output_path}")
        
        if not args.no_backup:
            log_info(f"Backup: {output_path}.bak")
    else:
        log_error("No se pudo completar la inyección")
        sys.exit(1)


if __name__ == '__main__':
    main()
