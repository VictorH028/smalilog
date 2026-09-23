"""Generadores de bloques de hook (enter / exit / d)."""

from smalilog.emit import box_scalar, const_null, indent, invoke_static, move_object
from ._types import is_reference


def generate_hook_enter(func_name, arg_name, arg_desc, arg_register, temps,
                        remote_logger_class: str):
    # Asumimos que `temps` trae al menos 2 temporales frescos para los strings.
    # Si requiere autoboxing de primitivos o null, usará el 3er temporal temps[2].
    t_name, t_argname = temps[0], temps[1]

    lines = [
        "# ========== HOOK ENTER ==========",
        f'const-string {t_name}, "{func_name}"',
        f'const-string {t_argname}, "{arg_name}"',
    ]

    if arg_desc is None:
        # Sin argumentos: pasar null
        t_val = temps[2]
        lines.append(const_null(t_val))
        target_reg = t_val
    elif is_reference(arg_desc):
        # Objeto/Referencia: pasar el registro original (ej. p0) directamente
        target_reg = arg_register
    else:
        # Tipo primitivo (int, boolean, etc.): requiere boxing hacia el 3er temporal
        t_val = temps[2]
        lines += box_scalar(arg_desc, arg_register, t_val)
        target_reg = t_val

    lines += [
        invoke_static(
            [t_name, t_argname, target_reg],
            f"{remote_logger_class}->hookEnter("
            f"Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V",
        ),
        "# ================================",
    ]
    return indent("\n".join(lines))
def generate_hook_exit(func_name, return_line, return_reg, temps, ret_type,
                       remote_logger_class: str):
    t_name, t_val = temps
    target = (f"{remote_logger_class}->hookExit("
              f"Ljava/lang/String;Ljava/lang/Object;)V")
    head = [
        "# ========== HOOK EXIT ==========",
        f'const-string {t_name}, "{func_name}"',
    ]

    # Caso 1: Retorno Void
    if return_line == "return-void" or return_reg is None:
        body = [f'const-string {t_val}, "void"']
        invoke = invoke_static(
            [t_name, t_val],
            f"{remote_logger_class}->hookExit(Ljava/lang/String;Ljava/lang/String;)V",
        )
        return indent("\n".join(head + body + [invoke, "# ================================"]))

    # Caso 2: Objeto / Referencia
    if return_line.startswith("return-object"):
        body = [move_object(t_val, return_reg)]
        
    # Caso 3: Primitivos Wide (double, long)
    elif return_line.startswith("return-wide"):
        body = box_scalar("D" if ret_type == "D" else "J", return_reg, t_val)
        
    # Caso 4: Primitivos Escalares (int, boolean, byte, char, float, short)
    else:
        body = box_scalar(ret_type if ret_type in ("F", "Z", "B", "C", "S") else "I", return_reg, t_val)

    return indent("\n".join(head + body + [
        invoke_static([t_name, t_val], target),
        "# ================================",
    ]))


def generate_d_log(tag, message, temps, remote_logger_class: str):
    t_tag, t_msg = temps
    return indent("\n".join([
        "# ========== LOG D ==========",
        f'const-string {t_tag}, "{tag}"',
        f'const-string {t_msg}, "{message}"',
        invoke_static(
            [t_tag, t_msg],
            f"{remote_logger_class}->d(Ljava/lang/String;Ljava/lang/String;)V",
        ),
        "# ============================",
    ]))
