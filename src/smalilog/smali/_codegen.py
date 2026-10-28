"""Generadores de bloques de hook (enter / exit / log)."""

from smalilog.emit import (
    _regnum,
    box_scalar,
    const_null,
    indent,
    invoke_static,
    move_object,
)
from ._types import is_reference


def _smali_string(value: object) -> str:
    """Escapa un valor para usarlo como literal de ``const-string``."""
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )


def _enter_temp_count(arg_desc: str | None) -> int:
    """Temps necesarios: 2 sin args, 3 con referencia y 4 con primitivo."""
    if arg_desc is None:
        return 2
    return 3 if is_reference(arg_desc) else 4


def generate_hook_enter(func_name, arg_desc, arg_register, temps,
                        remote_logger_class: str):
    """Genera la entrada invocando ``RemoteLog->traceIn(String, [Object)J``.

    El id de correlación devuelto se descarta; para la salida se usan las
    variantes sin id (``traceOut`` / ``traceOutVoid``).
    """
    required = _enter_temp_count(arg_desc)
    if len(temps) < required:
        raise ValueError(
            f"generate_hook_enter requiere {required} temporales, "
            f"recibidos {len(temps)}"
        )

    t_name, t_arr = temps[0], temps[1]

    lines = [
        "# ========== HOOK ENTER ==========",
        f'const-string {t_name}, "{_smali_string(func_name)}"',
    ]

    if arg_desc is None:
        # Sin argumentos: null como varargs de traceIn.
        lines.append(const_null(t_arr))
    else:
        # Object[1] con el primer argumento (o "this") dentro.
        t_idx = temps[2]
        lines += [
            f"const/4 {t_idx}, 0x1",
            f"new-array {t_arr}, {t_idx}, [Ljava/lang/Object;",
            f"const/4 {t_idx}, 0x0",
        ]

        if is_reference(arg_desc):
            lines.append(f"aput-object {arg_register}, {t_arr}, {t_idx}")
        else:
            # El boxeo usa un cuarto registro para no pisar el índice.
            t_boxed = temps[3]
            lines += box_scalar(arg_desc, arg_register, t_boxed)
            lines.append(f"aput-object {t_boxed}, {t_arr}, {t_idx}")

    lines += [
        invoke_static(
            [t_name, t_arr],
            f"{remote_logger_class}->traceIn("
            f"Ljava/lang/String;[Ljava/lang/Object;)J",
        ),
        "# ================================",
    ]
    return indent("\n".join(lines))


def generate_hook_exit(func_name, return_line, return_reg, temps, ret_type,
                       remote_logger_class: str):
    """Genera la salida invocando ``traceOutVoid`` o ``traceOut``.

    - ``RemoteLog->traceOutVoid(String)V`` para métodos void.
    - ``RemoteLog->traceOut(String, Object)V`` para métodos con retorno.
    """
    t_name, t_val = temps[0], temps[1]
    head = [
        "# ========== HOOK EXIT ==========",
        f'const-string {t_name}, "{_smali_string(func_name)}"',
    ]

    # Caso 1: retorno void.
    if return_line == "return-void" or return_reg is None:
        invoke = invoke_static(
            [t_name],
            f"{remote_logger_class}->traceOutVoid(Ljava/lang/String;)V",
        )
        return indent("\n".join(head + [invoke, "# ================================"]))

    # Caso 2: objeto / referencia.
    if return_line.startswith("return-object"):
        body = [move_object(t_val, return_reg)]

    # Caso 3: primitivos wide (double, long).
    elif return_line.startswith("return-wide"):
        body = box_scalar("D" if ret_type == "D" else "J", return_reg, t_val)

    # Caso 4: primitivos escalares (int, boolean, byte, char, float, short).
    else:
        body = box_scalar(
            ret_type if ret_type in ("F", "Z", "B", "C", "S") else "I",
            return_reg,
            t_val,
        )

    invoke = invoke_static(
        [t_name, t_val],
        f"{remote_logger_class}->traceOut(Ljava/lang/String;Ljava/lang/Object;)V",
    )

    return indent("\n".join(head + body + [invoke, "# ================================"]))


def generate_d_log_level(level: str, tag: str, message: str, temps,
                         remote_logger_class: str):
    """Genera un log de nivel fijo (d/i/w/e) con tag y mensaje constantes.

    Firma smali: ``(Ljava/lang/String;Ljava/lang/String;)V``.
    """
    level = level.lower()
    if level not in ("d", "i", "w", "e"):
        raise ValueError(f"nivel de log inválido: {level!r}")

    t_tag, t_msg = temps[0], temps[1]
    return indent("\n".join([
        f"# ========== LOG {level.upper()} ==========",
        f'const-string {t_tag}, "{_smali_string(tag)}"',
        f'const-string {t_msg}, "{_smali_string(message)}"',
        invoke_static(
            [t_tag, t_msg],
            f"{remote_logger_class}->{level}("
            f"Ljava/lang/String;Ljava/lang/String;)V",
        ),
        "# ============================",
    ]))


def _smali_int(value: int) -> str:
    """Formatea un entero como literal hexadecimal de Smali."""
    if value < 0:
        return f"-0x{-value:x}"
    return f"0x{value:x}"


def _const_instr(reg: str, value: int) -> str:
    """Emite la instrucción ``const`` más compacta para un registro."""
    n = _regnum(reg)
    if -8 <= value <= 7 and n <= 15:
        return f"const/4 {reg}, {_smali_int(value)}"
    if -32768 <= value <= 32767 and n <= 255:
        return f"const/16 {reg}, {_smali_int(value)}"
    if -(2 ** 31) <= value < 2 ** 31:
        return f"const {reg}, {_smali_int(value)}"
    raise ValueError(f"literal fuera de rango de 32 bits: {value}")


def _const_wide_instr(reg: str, value: int) -> str:
    """Emite la instrucción ``const-wide`` más compacta para un registro."""
    n = _regnum(reg)
    if -32768 <= value <= 32767 and n <= 255:
        return f"const-wide/16 {reg}, {_smali_int(value)}"
    if -(2 ** 63) <= value < 2 ** 63:
        return f"const-wide {reg}, {_smali_int(value)}"
    raise ValueError(f"literal fuera de rango de 64 bits: {value}")


def generate_return_stub(return_type: str, value, temps):
    """Genera un retorno constante al principio de un método.

    Se usa para traducir los ``onLeave return <literal>`` y
    ``args.skip = true`` de Renef a Smali estático.

    - ``V``: ``return-void`` (ignora ``value``).
    - ``J``/``D``: ``const-wide`` + ``return-wide``.
    - Referencia: ``const-string``/``null`` + ``return-object``.
    - Primitivo: ``const`` + ``return``.
    """
    if return_type == "V":
        return indent("return-void")

    if return_type in ("J", "D"):
        reg = temps[0]
        number = 0 if value is None else int(value)
        return indent("\n".join([
            _const_wide_instr(reg, number),
            f"return-wide {reg}",
        ]))

    if is_reference(return_type):
        reg = temps[0]
        if isinstance(value, str):
            body = [f'const-string {reg}, "{_smali_string(value)}"']
        else:
            body = [_const_instr(reg, 0)]
        body.append(f"return-object {reg}")
        return indent("\n".join(body))

    reg = temps[0]
    if isinstance(value, bool):
        number = 1 if value else 0
    else:
        number = 0 if value is None else int(value)
    return indent("\n".join([
        _const_instr(reg, number),
        f"return {reg}",
    ]))


def generate_trace_out_correlated(
    func_name: str, return_line: str, return_reg: str | None,
    trace_id_reg: str, temps, ret_type: str,
    remote_logger_class: str,
):
    """Genera salida con un traceId correlacionado.

    - void:   ``traceOutVoid(String, J)V``
    - objeto: ``traceOut(String, J, Object)V``
    - prim:   boxeo + ``traceOut(String, J, Object)V``

    Requiere 2 temps (nombre + valor).
    """
    t_name, t_val = temps[0], temps[1]

    head = [
        "# ========== HOOK EXIT (correlacionado) ==========",
        f'const-string {t_name}, "{_smali_string(func_name)}"',
    ]

    if return_line == "return-void" or return_reg is None:
        invoke = invoke_static(
            [t_name, trace_id_reg],
            f"{remote_logger_class}->traceOutVoid(Ljava/lang/String;J)V",
        )
        return indent("\n".join(head + [invoke, "# ================================"]))

    if return_line.startswith("return-object"):
        body = [move_object(t_val, return_reg)]
    elif return_line.startswith("return-wide"):
        body = box_scalar("D" if ret_type == "D" else "J", return_reg, t_val)
    else:
        body = box_scalar(ret_type if ret_type in ("F", "Z", "B", "C", "S") else "I",
                          return_reg, t_val)

    invoke = invoke_static(
        [t_name, trace_id_reg, t_val],
        f"{remote_logger_class}->traceOut("
        f"Ljava/lang/String;JLjava/lang/Object;)V",
    )
    return indent("\n".join(head + body + [invoke, "# ================================"]))


def generate_trace_out_error(
    func_name: str, exc_reg: str, trace_id_reg: str | None,
    temps, remote_logger_class: str, correlated: bool = False,
):
    """Genera la salida por excepción.

    - sin id: ``traceOutError(String, Throwable)V``
    - con id: ``traceOutError(String, J, Throwable)V``

    Requiere 1 temp (nombre).
    """
    t_name = temps[0]
    head = [
        "# ========== HOOK EXIT ERROR ==========",
        f'const-string {t_name}, "{_smali_string(func_name)}"',
    ]
    if correlated and trace_id_reg is not None:
        invoke = invoke_static(
            [t_name, trace_id_reg, exc_reg],
            f"{remote_logger_class}->traceOutError("
            f"Ljava/lang/String;JLjava/lang/Throwable;)V",
        )
    else:
        invoke = invoke_static(
            [t_name, exc_reg],
            f"{remote_logger_class}->traceOutError("
            f"Ljava/lang/String;Ljava/lang/Throwable;)V",
        )
    return indent("\n".join(head + [invoke, "# ================================"]))
