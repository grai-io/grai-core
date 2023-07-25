import os
import subprocess
import tempfile
import time
import webbrowser
from functools import cached_property
from typing import Optional

import requests
import typer
from pydantic import BaseModel

from grai_cli.api.demo.setup import demo_app
from grai_cli.utilities.utilities import print


class Demo:
    default_url = "https://raw.githubusercontent.com/grai-io/grai-core/master/examples/deployment/docker-compose/demo/docker-compose.yaml"

    def __init__(self, file: Optional[str] = None, url: Optional[str] = None):
        self.file = file
        self.url = self.default_url if url is None else url
        self.check_for_docker_and_docker_compose()

    @staticmethod
    def check_for_docker_and_docker_compose():
        try:
            docker_version = subprocess.check_output(["docker", "--version"], text=True)
            docker_compose_version = subprocess.check_output(["docker-compose", "--version"], text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(
                "Docker and/or Docker Compose is not installed. You can find more information about installing docker "
                "here: https://docs.docker.com/engine/install/"
            ) from e

    @cached_property
    def compose_script(self) -> str:
        if self.file is not None:
            with open(self.file, "r") as f:
                result = f.read()
            return result

        resp = requests.get(self.url, allow_redirects=True)
        if resp.status_code != 200:
            raise Exception(
                f"We were unable to fetch the deployment script from github. Our attempt returned a {resp.status_code} "
                f"error code with the message `{resp.reason}`."
            )
        return resp.text

    @staticmethod
    def run_command(file_name) -> list:
        return ["docker", "compose", "-f", file_name, "up", "-d"]

    @staticmethod
    def stop_command(file_name) -> list:
        return ["docker", "compose", "-f", file_name, "down"]

    def stop_script(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(self.compose_script.encode())
        try:
            subprocess.run(self.stop_command(temp.name))
        finally:
            os.unlink(temp.name)

    def run_script(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(self.compose_script.encode())
        try:
            subprocess.run(self.run_command(temp.name))
        finally:
            os.unlink(temp.name)

        # Wait for the containers to be up and running
        max_attempts = 30
        attempt = 0
        while attempt < max_attempts:
            try:
                response = requests.get("http://localhost:3000")
                response.raise_for_status()
                print("\n🎉🎉🎉 Containers are up and running! 🎉🎉🎉\n")
                break
            except requests.exceptions.RequestException:
                print("Waiting for containers to start...")
                time.sleep(5)
                attempt += 1
        else:
            print("Containers took too long to start. Exiting.")
            return

        print(f"LOGIN INFORMATION\n" "--------------------\n" f"Username: null@grai.io\n" f"Password: super_secret")
        # Give the user a chance to see the login information
        time.sleep(3)

        # Open the browser to localhost:3000
        webbrowser.open("http://localhost:3000")


@demo_app.command("start", help="Run the demo environment")
def start_demo(compose_file: Optional[str] = typer.Argument(None)):
    demo = Demo(file=compose_file)
    demo.run_script()


@demo_app.command("stop", help="Stop the demo environment")
def stop_demo(compose_file: Optional[str] = typer.Argument(None)):
    demo = Demo(file=compose_file)
    demo.stop_script()
