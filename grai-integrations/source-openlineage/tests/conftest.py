import json
import os
from typing import Callable

import pytest
from grai_schemas.v1.mock import MockV1
from grai_schemas.v1.organization import OrganisationV1
from grai_schemas.v1.source import SourceV1
from grai_schemas.v1.workspace import WorkspaceV1


@pytest.fixture(scope="session")
def tests_data_path() -> str:
    return os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture(scope="session")
def openlineage_test_event(tests_data_path) -> dict:
    return json.load(open(os.path.join(tests_data_path, "event.json")))


@pytest.fixture(scope="session")
def mock_organisation() -> OrganisationV1:
    return MockV1().organisation.organisation()


@pytest.fixture(scope="session")
def mock_workspace(mock_organisation) -> WorkspaceV1:
    return MockV1(organisation=mock_organisation).workspace.workspace()


@pytest.fixture(scope="session")
def mock_source(mock_workspace) -> SourceV1:
    return MockV1(workspace=mock_workspace).source.source()


@pytest.fixture(scope="session")
def mocker(mock_workspace, mock_source, mock_organisation) -> MockV1:
    return MockV1(workspace=mock_workspace, data_source=mock_source, organisation=mock_organisation)


class DataGetter:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.available_data = {os.path.basename(x[0]): x[0] for x in os.walk(self.data_path)}

    def get(self, name: str) -> dict:
        if name not in self.available_data:
            raise ValueError(f"Data {name} not available. Available data: {self.available_data}")
        return json.load(open(os.path.join(self.available_data[name], f"1.json")))


@pytest.fixture(scope="session")
def test_data_getter(tests_data_path) -> DataGetter:
    return DataGetter(tests_data_path)
