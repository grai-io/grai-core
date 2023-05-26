import datetime
import uuid
from typing import get_args

import pytest

from grai_client.endpoints.client import validate_connection_arguments
from grai_client.endpoints.utilities import add_query_params, serialize_obj


def make_v1_node():
    return {
        "type": "Node",
        "version": "v1",
        "spec": {
            "id": uuid.uuid4(),
            "name": "test",
            "namespace": "test-ns",
            "data_source": "tests",
            "display_name": "ouch",
            "is_active": True,
            "metadata": {
                "test_dict": {"a": "b"},
                "test_list": [1, 2, 3],
                "test_tuple": (4, 5, 6),
                "test_date": datetime.date(2021, 3, 14),
            },
        },
    }


def test_serialize_obj():
    obj = make_v1_node()
    json = serialize_obj(obj)
    assert isinstance(json, (str, bytes)), type(json)


class TestAddQueryParams:
    def test_add_query_params_no_initial_query(self):
        url = "www.grai.io"
        params = {"okay": "computer"}
        new_url = add_query_params(url, params)
        assert new_url == "www.grai.io?okay=computer"

    def test_add_query_params_no_initial_query_trailing_slash(self):
        url = "www.grai.io/"
        params = {"okay": "computer"}
        new_url = add_query_params(url, params)
        assert new_url == "www.grai.io/?okay=computer"

    def test_add_query_params_with_initial_query(self):
        url = "www.grai.io/?weird=fishes"
        params = {"okay": "computer"}
        new_url = add_query_params(url, params)
        assert new_url == "www.grai.io/?weird=fishes&okay=computer"


@pytest.mark.filterwarnings("error")
class TestCredentialValidation:
    @pytest.mark.xfail
    def test_incompatible_proto_insecure(self):
        validate_connection_arguments(host="api.grai.io", protocol="https", insecure=True)

    @pytest.mark.xfail
    def test_incompatible_proto_insecure2(self):
        validate_connection_arguments(host="api.grai.io", protocol="http", insecure=False)

    @pytest.mark.xfail
    def test_invalid_port(self):
        validate_connection_arguments(host="api.grai.io", protocol="https", insecure=True, port="apple")

    def test_default_insecure_protocol(self):
        _, _, _, proto, _ = validate_connection_arguments(host="api.grai.io", insecure=True)
        assert proto == "http", "Insecure was set to True but protocol is not http"

    def test_default_secure_protocol(self):
        _, _, _, proto, _ = validate_connection_arguments(host="api.grai.io", insecure=False)
        assert proto == "https", "Insecure was set to False but protocol is not https"

    def test_default_protocol(self):
        _, _, _, proto, _ = validate_connection_arguments(host="api.grai.io")
        assert proto == "https", "Protocol was not https by default"

    @pytest.mark.xfail
    def test_unsupported_protocol(self):
        _, _, _, proto, _ = validate_connection_arguments(host="api.grai.io", protcol="ftp")

    def test_default_insecure(self):
        _, _, _, _, insecure = validate_connection_arguments(host="api.grai.io")
        assert insecure is False, "`insecure` was not set to False by default"

    def test_default_port(self):
        _, _, port, _, _ = validate_connection_arguments(host="api.grai.io")
        assert port is None, f"`port` should default to None not {port} when the host is something other than localhost"

    def test_default_localhost_port(self):
        _, _, port, _, _ = validate_connection_arguments(host="localhost")
        assert port == "8000", f"`port` should default to '8000' not {port} when host='localhost'"

    def test_build_url_with_proto_host_port(self):
        url, _, _, _, _ = validate_connection_arguments(protocol="http", host="localhost", port="8000")
        message = f"Expected url='http://localhost:8000' not {url}"
        assert url == "http://localhost:8000", message

    def test_build_url_with_proto_host(self):
        url, _, _, _, _ = validate_connection_arguments(protocol="http", host="api.grai.io")
        message = f"Expected url='http://api.grai.io' not {url}"
        assert url == "http://api.grai.io", message

    def test_build_url_with_host(self):
        url, _, _, _, _ = validate_connection_arguments(host="api.grai.io")
        message = f"Expected url='https://api.grai.io' not {url}"
        assert url == "https://api.grai.io", message

    def test_url_no_host(self):
        url, _, _, _, _ = validate_connection_arguments(url="https://api.grai.io")

    def test_host_no_url(self):
        url, _, _, _, _ = validate_connection_arguments(host="api.grai.io")

    @pytest.mark.xfail
    def test_no_host_no_url(self):
        url, _, _, _, _ = validate_connection_arguments()

    @pytest.mark.xfail
    def test_invalid_insecure_value(self):
        _, _, _, _, insecure = validate_connection_arguments(host="api.grai.io", insecure="purple")

    def test_url_parsed_url(self):
        test_url = "http://app.grai.io:8000"
        url, host, port, protocol, insecure = validate_connection_arguments(url=test_url)
        assert url == test_url, f"Validated url {url} did not match expected url {test_url}"

    def test_url_parsed_host(self):
        result = "app.grai.io"
        url, host, port, protocol, insecure = validate_connection_arguments(url="http://app.grai.io:8000")
        assert host == result, f"Validated url {url} did not match expected url {result}"

    def test_url_parsed_port(self):
        result = "8000"
        url, host, port, protocol, insecure = validate_connection_arguments(url="http://app.grai.io:8000")
        assert port == result, f"Validated port {port} did not match expected url {result}"

    def test_url_parsed_no_port(self):
        result = None
        url, host, port, protocol, insecure = validate_connection_arguments(url="http://app.grai.io")
        assert port is None, f"Validated port {port} did not match expected url {result}"

    def test_url_parsed_insecure(self):
        result = True
        url, host, port, protocol, insecure = validate_connection_arguments(url="http://app.grai.io")
        assert insecure == result, f"Validated insecure {insecure} did not match expected url {result}"

    def test_url_parsed_secure(self):
        result = False
        url, host, port, protocol, insecure = validate_connection_arguments(url="https://app.grai.io")
        assert insecure == result, f"Validated insecure {insecure} did not match expected url {result}"

    def test_url_parsed_protocol(self):
        result = "http"
        url, host, port, protocol, insecure = validate_connection_arguments(url="http://app.grai.io:8000")
        assert protocol == result, f"Validated protocol {protocol} did not match expected url {result}"
