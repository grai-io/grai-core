import requests

from grai_cli.api.demo.setup import demo_app


@demo_app.command("run", help="Run the demo environment")
def run_demo():
    """"""
    url = ""
