import ast
import copy
import os
import re
from typing import Dict, List

num_spaces = 4
SPACES = " " * num_spaces
DEFAULT_ATTR_STRING = "todo"


class ClassVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.classes_with_attributes = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        for item in node.body:
            if isinstance(item, ast.AnnAssign):
                self.classes_with_attributes.append(node)
                break
        self.generic_visit(node)


def get_classes_with_attributes(file_path: str):
    """Returns classes with attribute definitions from a given Python file."""
    with open(file_path, "r") as f:
        source = f.read()

    tree = ast.parse(source)
    visitor = ClassVisitor()
    visitor.visit(tree)

    return visitor.classes_with_attributes


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
    classes = get_classes_with_attributes(filename)

    source = "".join(lines).split("\n")
    new_source = source.copy()
    offset = 0  # Keep track of the lines added for accurate insertion of subsequent docstrings

    for class_node in classes:
        current_doc = ast.get_docstring(class_node, clean=False)

        existing_descriptions = extract_attribute_descriptions(current_doc)
        default_description = f"Class definition of {class_node.name}"
        # Extract attributes using annotations
        attributes = [item.target.id for item in class_node.body if isinstance(item, ast.AnnAssign)]
        attr_map = {attr: existing_descriptions.get(attr, DEFAULT_ATTR_STRING) for attr in attributes}
        attr_map = {k: DEFAULT_ATTR_STRING if v.strip().isspace() else v for k, v in attr_map.items()}

        attributes_str = "\n".join([f"{SPACES * 2}{k}: {v}" for k, v in attr_map.items()])
        attributes_docstring = f"{SPACES}Attributes:\n{attributes_str}".rstrip()

        doc_line = class_node.lineno - 1  # -1 because lineno is 1-based

        if current_doc is not None:
            split_str = f"{SPACES}Attributes:\n"
            doc_parts = current_doc.split(split_str)

            assert len(doc_parts) <= 2, f"Docstring has unexpected format, multiple `{split_str}` found"

            if len(doc_parts) == 1:
                current_description = current_doc.rstrip()
                post_attribute_string = ""
            elif len(doc_parts) == 2:
                second_part = doc_parts[1].split(f"\n{SPACES * 2}")[-1]
                post_attribute_string = second_part[second_part.index("\n") :].rstrip()
                current_description = current_doc[: current_doc.index(split_str)].rstrip()

            description = f"{default_description}\n" if current_description == "" else f"{current_description}\n"
            docstring = f'{SPACES}"""{description}\n{attributes_docstring}\n{post_attribute_string}\n{SPACES}"""'

            doc_start_line = next(i for i, line in enumerate(source[doc_line:]) if '"""' in line) + doc_line
            idx = doc_start_line + offset
            if source[doc_start_line].count('"""') == 2:
                new_source[idx] = docstring
            else:
                end_idx = (
                    next(i for i, line in enumerate(source[doc_start_line + 1 :]) if '"""' in line) + doc_start_line + 1
                ) + offset

                new_source = new_source[:idx] + [docstring] + new_source[end_idx + 1 :]
        else:
            docstring = f'{SPACES}"""{default_description}\n{attributes_docstring}\n{SPACES}"""'
            new_doc_line = doc_line + offset
            new_source = new_source[: new_doc_line + 1] + [docstring] + new_source[new_doc_line + 1 :]

        offset = len(new_source) - len(source)

    new_source = "\n".join(new_source)
    with open(filename, "w") as file:
        file.write(new_source)


if __name__ == "__main__":
    directory = os.path.join(os.path.dirname(__file__), "..", "src", "grai_schemas")
    # directory = "."
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                add_google_style_docstring(filepath)
