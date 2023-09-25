import ast
import copy
import os
import re
from typing import Dict, List

num_spaces = 4
SPACES = " " * num_spaces


class PydanticBaseModelVisitor(ast.NodeVisitor):
    def __init__(self):
        self.classes: List[ast.ClassDef] = []
        self.imported_pydantic = False
        self.imported_directly = False

    def visit_Import(self, node: ast.Import):
        for n in node.names:
            if n.name == "pydantic":
                self.imported_pydantic = True
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module == "pydantic":
            for n in node.names:
                if n.name == "BaseModel":
                    self.imported_directly = True
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == "BaseModel" and self.imported_directly:
                self.classes.append(node)
            elif isinstance(base, ast.Attribute) and base.attr == "BaseModel" and self.imported_pydantic:
                if isinstance(base.value, ast.Name) and base.value.id == "pydantic":
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
    offset = 0  # Keep track of the lines added for accurate insertion of subsequent docstrings

    for class_node in visitor.classes:
        current_doc = ast.get_docstring(class_node)
        existing_descriptions = extract_attribute_descriptions(current_doc)

        # Extract attributes using annotations
        attributes = [item.target.id for item in class_node.body if isinstance(item, ast.AnnAssign)]
        attributes_str = "\n".join(
            [f"{SPACES}{SPACES}{attr}: {existing_descriptions.get(attr, f'')}" for attr in attributes]
        )
        attributes_docstring = f"{SPACES}Attributes:\n{attributes_str}"

        doc_line = class_node.lineno - 1  # -1 because lineno is 1-based

        if current_doc:
            split_str = f"Attributes:\n"
            doc_parts = current_doc.split(split_str)

            assert len(doc_parts) <= 2, f"Docstring has unexpected format, multiple `{split_str}` found"

            if len(doc_parts) == 1:
                current_description = f"\n{SPACES}".join(doc_parts[0].split("\n")) + "\n\n"
                post_attribute_string = ""
            elif len(doc_parts) == 2:
                second_part = doc_parts[1].split("\n")
                for i, part in enumerate(second_part):
                    if not part.startswith(SPACES):
                        break

                if i == len(second_part) - 1:
                    post_attribute_string = ""
                else:
                    post_attribute_string = f"".join([f"\n{SPACES}{part}" for part in second_part[i:]])
                current_description = f"\n{SPACES}".join(doc_parts[0].split("\n")).rstrip(SPACES)

            docstring = f'{SPACES}"""{current_description}{attributes_docstring}{post_attribute_string}\n{SPACES}"""'
            doc_start_line = next(i for i, line in enumerate(source[doc_line:]) if '"""' in line) + doc_line
            doc_end_line = (
                next(i for i, line in enumerate(source[doc_start_line + 1 :]) if '"""' in line) + doc_start_line + 1
            )
            new_source = new_source[: doc_start_line + offset] + [docstring] + new_source[doc_end_line + offset + 1 :]
        else:
            docstring = f'{SPACES}"""\n{attributes_docstring}\n{SPACES}"""'
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
