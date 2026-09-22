"""Emisión de código y artefactos."""
from ._emit import box_scalar, const_null, indent, invoke_static, move_object, move_result_object

__all__ = [
        "box_scalar", 
        "const_null", 
        "indent",
        "invoke_static",
        "move_object",
        "move_result_object"]
