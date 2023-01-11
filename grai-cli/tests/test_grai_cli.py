from typer.testing import CliRunner

from grai_cli.api.entrypoint import app
from grai_cli.settings.cache import cache
from grai_cli.utilities.test import prep_tests

prep_tests()
runner = CliRunner()


def test_disable_telemetry():
    result = runner.invoke(app, ["--no-telemetry"])
    telemetry = cache.get("telemetry_consent")
    assert not telemetry


def test_enable_telemetry():
    result = runner.invoke(app, ["--telemetry"])
    telemetry = cache.get("telemetry_consent")
    assert telemetry


#
# def test_version():
#     assert __version__ == "0.1.0"
