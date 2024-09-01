from pathlib import Path as _Path

import pyserials as _ps


RESERVED_PYTHON_KEYWORDS = [
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
    'break', 'class', 'continue', 'def', 'del', 'elif', 'else',
    'except', 'finally', 'for', 'from', 'global', 'if', 'import',
    'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise',
    'return', 'try', 'while', 'with', 'yield'
]


VOID_CLASS = """
class {class_name}(VoidElement):
    def __init__(self, attrs: AttrsType | None = None):
        super().__init__(name="{elem_name}", attrs=attrs)
        return
"""

VOID_FUNC = """
def {function_name}(attrs: AttrsType | None = None, /, **keyword_attrs) -> {class_name}:
    return {class_name}((attrs or {{}}) | keyword_attrs)
"""

CONTENT_CLASS = """
class {class_name}(ContentElement):
    def __init__(self, content: Container, attrs: AttrsType | None = None):
        super().__init__(name="{elem_name}", content=content, attrs=attrs)
        return
"""

CONTENT_FUNC = """
def {function_name}(
    content: ContentInputType = None, attrs: AttrsType | None = None, /, **keyword_attrs
) -> {class_name}:
    return {class_name}(content=htmp.container_from_object(content), attrs=(attrs or {{}}) | keyword_attrs)
"""


def generate_file_content(html_elements_data: dict[str, dict]):
    classes = []
    functions = []
    for elem_name, elem_data in sorted(html_elements_data.items()):
        func_name = elem_name
        class_name = elem_name.upper()
        if func_name in RESERVED_PYTHON_KEYWORDS:
            func_name += "_"
        if class_name in RESERVED_PYTHON_KEYWORDS:
            class_name += "_"
        template_keywords = {
            "elem_name": elem_name,
            "class_name": class_name,
            "function_name": func_name,
        }
        if elem_data.get("void", False):
            class_template = VOID_CLASS
            func_template = VOID_FUNC
        else:
            class_template = CONTENT_CLASS
            func_template = CONTENT_FUNC
        classes.append(class_template.format(**template_keywords).strip())
        functions.append(func_template.format(**template_keywords).strip())
    return "\n\n\n".join(classes + functions)


def generate(package_path: str | _Path):
    html_elements_data_filepath = _Path(package_path) / "data" / "html" / "elements.yaml"
    html_elements_data = _ps.read.yaml_from_file(html_elements_data_filepath)
    file_content = generate_file_content(html_elements_data)
    output_path = _Path(package_path) / "html" / "el.py"
    output_path.write_text(file_content)
    return
