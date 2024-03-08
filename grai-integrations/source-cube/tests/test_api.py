from grai_source_cube.api import MetaResponseSchema
from pytest_cases import parametrize_with_cases


class IntegrationCases:
    """
    Run tests when possible for cube cloud, cube core, and our mocks
    """

    @staticmethod
    def case_cube_core(local_integration):
        return local_integration

    @staticmethod
    def case_cube_cloud(mock_integration):
        return mock_integration

    @staticmethod
    def case_mock_api(cloud_integration):
        return cloud_integration


@parametrize_with_cases("test_integration", cases=IntegrationCases, filter=lambda x: x is not None)
def test_api_ready_endpoint(test_integration):
    assert test_integration.connector.ready().status_code == 200


@parametrize_with_cases("test_integration", cases=IntegrationCases, filter=lambda x: x is not None)
def test_api_meta_endpoint(test_integration):
    assert isinstance(test_integration.connector.meta(), MetaResponseSchema)
