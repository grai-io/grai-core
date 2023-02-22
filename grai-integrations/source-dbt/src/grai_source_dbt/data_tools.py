import os

import pkg_resources

from grai_source_dbt.processor import ManifestProcessor

file_id_map = {"jaffle_shop": "manifest.json"}


def get_project_root() -> str:
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def get_manifest_file(file_id: str = "jaffle_shop") -> str:
    if file_id not in file_id_map:
        raise Exception(
            f"Unrecognized file name identifier: {file_id}. Currently supported manifest files include {list(file_id_map.keys())}"
        )
    filename = pkg_resources.resource_filename(__name__, os.path.join("data", file_id_map[file_id]))
    return filename


def load_from_manifest() -> ManifestProcessor:
    manifest = ManifestProcessor.load(get_manifest_file(), "default")
    return manifest
