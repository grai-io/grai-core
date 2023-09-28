import os
import tomllib

from grai_client import __version__


def test_correct_version():
    toml_file = os.path.join(os.path.dirname(__file__), "../pyproject.toml")
    with open(toml_file, "rb") as f:
        pyproject = tomllib.load(f)

    version = pyproject["tool"]["poetry"]["version"]
    assert version == __version__
