```
injector/
├── __init__.py
├── hooker.py                 # Fachada pública + run_hooker (CLI entry)
├── _colors.py                # Color, _c, _USE_COLOR, log_*
├── _highlight.py             # Resaltado de sintaxis (pygments + fallback)
├── _smali_types.py           # Tipos, parse_type_list, _type_size, etc.
├── _smali_model.py           # SmaliMethod, count_parameter_registers, normalize_reg
├── _smali_parser.py          # parse_smali_file, _parse_method_line, parse_class_name
├── _register_planner.py      # plan_hook_registers
├── _emit.py                  # Helpers de emisión (_invoke_static, _move_object, _box_scalar, indent)
├── _codegen.py               # generate_hook_enter / exit / d_log
├── _injector.py              # HookInjector
├── _analyze.py               # analyze_method
└── _cli.py                   # build_hook_parser, run_hooker, show_method_source
```
