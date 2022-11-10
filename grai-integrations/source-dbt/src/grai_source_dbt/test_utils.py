import os
from functools import cache

from grai_source_dbt.loader import DBTGraph, Manifest


def get_manifest_file():
    filename = os.path.join(
        os.path.dirname(__file__), "..", "..", "tests", "data", "manifest.json"
    )
    return filename


@cache
def load_from_manifest():
    manifest = Manifest.load(get_manifest_file())
    return manifest


@cache
def load_dbt_graph():
    manifest = load_from_manifest()
    dbt_graph = DBTGraph(manifest)
    return dbt_graph
