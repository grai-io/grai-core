import os

import pkg_resources

from grai_source_dbt.loader import DBTGraph, Manifest

file_id_map = {"jaffle_shop": "manifest.json"}


def get_manifest_file(file_id: str = "jaffle_shop") -> str:
    if file_id not in file_id_map:
        raise Exception(
            f"Unrecognized file name identifier: {file_id}. Currently supported manifest files include {list(file_id_map.keys())}"
        )
    filename = pkg_resources.resource_filename(__name__, os.path.join("data", file_id_map[file_id]))
    return filename


def load_from_manifest() -> Manifest:
    manifest = Manifest.load(get_manifest_file())
    return manifest


def load_dbt_graph() -> DBTGraph:
    manifest = load_from_manifest()
    dbt_graph = DBTGraph(manifest)

    return dbt_graph
