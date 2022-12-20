import os

import pkg_resources
from grai_source_dbt.loader import DBTGraph, Manifest


def get_manifest_file() -> str:
    filename = pkg_resources.resource_filename(
        __name__, os.path.join("data", "manifest.json")
    )
    return filename


def load_from_manifest() -> Manifest:
    manifest = Manifest.load(get_manifest_file())
    return manifest


def load_dbt_graph() -> DBTGraph:
    manifest = load_from_manifest()
    dbt_graph = DBTGraph(manifest)
    return dbt_graph
