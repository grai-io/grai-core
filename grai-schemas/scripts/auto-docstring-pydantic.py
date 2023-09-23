import ast
import copy
import os
import re
from typing import Dict, List


class PydanticBaseModelVisitor(ast.NodeVisitor):
    def __init__(self):
        self.classes: List[ast.ClassDef] = []

    def visit_ClassDef(self, node: ast.ClassDef):
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == "BaseModel":
                self.classes.append(node)
            elif isinstance(base, ast.Attribute) and base.attr == "BaseModel":
                self.classes.append(node)
        self.generic_visit(node)


def extract_attribute_descriptions(docstring: str) -> Dict[str, str]:
    """Extract attribute descriptions from a docstring."""
    descriptions = {}
    if not docstring:
        return descriptions

    lines = iter(docstring.split("\n"))
    for line in lines:
        match = re.match(r"\s+([a-zA-Z_]\w*):\s*(.*)", line)
        if match:
            attr, desc = match.groups()
            descriptions[attr] = desc.strip()

    return descriptions


def add_google_style_docstring(filename: str):
    with open(filename, "r") as file:
        lines = file.readlines()

    tree = ast.parse("".join(lines))
    visitor = PydanticBaseModelVisitor()
    visitor.visit(tree)

    source = "".join(lines).split("\n")
    new_source = source.copy()
    insert_offsets = 0  # Keep track of the lines added for accurate insertion of subsequent docstrings

    for class_node in visitor.classes:
        current_doc = ast.get_docstring(class_node)
        existing_descriptions = extract_attribute_descriptions(current_doc)

        docstring_content = f"This class represents {class_node.name}."

        # Extract attributes using annotations
        attributes = [item.target.id for item in class_node.body if isinstance(item, ast.AnnAssign)]
        attributes_str = "\n".join(
            [f"        {attr}: {existing_descriptions.get(attr, f'Description of {attr}.')}" for attr in attributes]
        )

        docstring = f'    """\n    {docstring_content}\n\n    Attributes:\n{attributes_str}\n    """'

        class_line = class_node.lineno - 1  # -1 because lineno is 1-based
        new_class_line = class_line + insert_offsets
        if current_doc:
            doc_start_line = next(i for i, line in enumerate(source[class_line:]) if '"""' in line) + class_line
            doc_end_line = (
                next(i for i, line in enumerate(source[doc_start_line + 1 :]) if '"""' in line) + doc_start_line + 1
            )
            new_source = new_source[:doc_start_line] + [docstring] + new_source[doc_end_line + 1 :]
            insert_offsets = len(new_source) - len(source)
        else:
            breakpoint()
            new_source = new_source[:class_line] + [docstring] + new_source[class_line + 1 :]
            insert_offsets += len(docstring.split("\n"))

    new_source = "\n".join(new_source)
    with open(filename, "w") as file:
        file.write(new_source)


if __name__ == "__main__":
    directory = "."

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and file == "test.py":
                filepath = os.path.join(root, file)
                add_google_style_docstring(filepath)
