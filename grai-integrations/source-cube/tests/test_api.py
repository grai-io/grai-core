from typing import Optional

from grai_source_cube.api import MetaResponseSchema
from grai_source_cube.base import CubeIntegration
from pytest_cases import parametrize_with_cases


class IntegrationCases:
    """
    Run tests when possible for cube cloud, cube core, and our mocks
    """

    @staticmethod
    def case_cube_core(local_integration) -> Optional[CubeIntegration]:
        return local_integration

    @staticmethod
    def case_cube_cloud(mock_integration) -> Optional[CubeIntegration]:
        return mock_integration

    @staticmethod
    def case_mock_api(cloud_integration) -> Optional[CubeIntegration]:
        return cloud_integration


@parametrize_with_cases("test_integration", cases=IntegrationCases)
def test_connector_ready_endpoint(test_integration):
    if test_integration is None:
        return
    assert test_integration.connector.ready().status_code == 200


@parametrize_with_cases("test_integration", cases=IntegrationCases)
def test_integration_ready_endpoint(test_integration):
    if test_integration is None:
        return
    assert test_integration.ready() is True


@parametrize_with_cases("test_integration", cases=IntegrationCases)
def test_api_meta_endpoint(test_integration):
    if test_integration is None:
        return
    assert isinstance(test_integration.connector.meta(), MetaResponseSchema)
