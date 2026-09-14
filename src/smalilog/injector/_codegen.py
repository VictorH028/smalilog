"""Generadores de bloques de hook (enter / exit / d)."""
from __future__ import annotations

from ._emit import box_scalar, const_null, indent, invoke_static, move_object
from ._smali_types import is_reference


def generate_hook_enter(func_name, arg_name, arg_desc, arg_register, temps,
                        remote_logger_class: str):
    t_name, t_argname, t_val = temps
    lines = [
        "# ========== HOOK ENTER ==========",
        f'const-string {t_name}, "{func_name}"',
        f'const-string {t_argname}, "{arg_name}"',
    ]
    if arg_desc is None:
        lines.append(const_null(t_val))
    elif is_reference(arg_desc):
        lines.append(move_object(t_val, arg_register))
    else:
        lines += box_scalar(arg_desc, arg_register, t_val)
    lines += [
        invoke_static(
            [t_name, t_argname, t_val],
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

    if return_line == "return-void" or return_reg is None:
        body = [f'const-string {t_val}, "void"']
        invoke = invoke_static(
            [t_name, t_val],
            f"{remote_logger_class}->d(Ljava/lang/String;Ljava/lang/String;)V",
        )
        return indent("\n".join(head + body + [invoke,
                                               "# ================================"]))

    if return_line.startswith("return-object"):
        body = [move_object(t_val, return_reg)]
    elif return_line.startswith("return-wide"):
        body = box_scalar("D" if ret_type == "D" else "J", return_reg, t_val)
    else:
        body = box_scalar("F" if ret_type == "F" else "I", return_reg, t_val)

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
