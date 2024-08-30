import os
import subprocess
import tempfile

from grai_cli.api.demo.endpoints import Demo


class TestDemoRunner:
    demo = Demo()

    def test_get_compose(self):
        assert isinstance(self.demo.compose_script, str)

    def test_compose_script_is_valid(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(self.demo.compose_script.encode())

        try:
            result = subprocess.run(["docker", "compose", "-f", temp.name, "config"], capture_output=True, text=True)
        finally:
            os.unlink(temp.name)
        assert result.returncode == 0, result.stderr

    def test_compose_up(self):
        pass
