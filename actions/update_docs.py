"""
Automatically updates the documentation for Grai's GitHub actions.

WARNING:
    * This script will overwrite any changes made to the documentation
    * mdx is not fully compatible with md so if a page fails to render this is likely the cause.
"""
import json
import os
import re

import yaml

action_root = "./grai-actions"
core_actions_docs_root = "../docs/pages/tooling/github-actions"

documented_file = os.path.join(action_root, "docs/documented.yaml")
with open(documented_file) as f:
    documented = yaml.safe_load(f)["ready"]


def make_header(doc):
    name = doc.get("name", doc["folder"])
    default_description = f"Documentation for Grai's {name} GitHub action."
    items = [
        "---",
        f"title: {doc.get('header_title', name)}",
        f"description: {doc.get('description', default_description)}",
        "---",
    ]
    header_string = "\n".join(items)
    return header_string


def write_doc_file(str_obj, path):
    with open(path, "w") as f:
        output = re.sub("<!--.*?-->", "", str_obj)
        f.write(output)


for doc in documented:
    readme_file = os.path.join(action_root, doc["folder"], "README.md")
    readme = open(readme_file).read()

    output_file = os.path.join(core_actions_docs_root, f"{doc['folder']}.md")
    new_readme = f"{make_header(doc)}\n\n{readme}"
    write_doc_file(new_readme, output_file)

base_readme = os.path.join(action_root, "base_readme.md")
base_readme = open(base_readme).read()

index_header_items = ["---", "title: Grai Actions", "description: Documentation for Grai's GitHub actions.", "---"]
index_header = "\n".join(index_header_items)
index_readme = f"{index_header}\n\n{base_readme}"

index_file = f"{core_actions_docs_root}.md"
write_doc_file(index_readme, index_file)

_meta_json = {doc["folder"]: doc.get("name", doc["folder"]) for doc in documented}
with open(os.path.join(core_actions_docs_root, "_meta.json"), "w") as f:
    json.dump(_meta_json, f)
