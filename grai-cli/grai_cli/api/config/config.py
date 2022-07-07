import typer
from grai_cli.api.config.setup import config_app
from grai_cli import config
from grai_cli.utilities.styling import default_styler
from grai_cli.utilities.validators import username_callback, password_callback, host_callback, port_callback, default_style_stripper
from grai_cli.utilities.utilities import writes_config


@config_app.command('init')
@writes_config
def cli_init_config(
    username: str = typer.Option(default=default_styler(config['auth']['user'].get(str)),
                                 prompt=True,
                                 callback=default_style_stripper(username_callback),
                                 prompt_required=True),
    password: str = typer.Option(..., prompt=True,
                                 prompt_required=True,
                                 hide_input=True,
                                 confirmation_prompt=True,
                                 callback=default_style_stripper(password_callback)),
    host: str = typer.Option(default=default_styler(config['server']['host'].get(str)),
                             prompt="Server host",
                             prompt_required=True,
                             callback=default_style_stripper(host_callback)),
    port: str = typer.Option(default=default_styler(config['server']['port'].get(str)),
                             prompt="Server port",
                             prompt_required=True,
                             callback=default_style_stripper(port_callback)),
    config_location: str = typer.Option(default=default_styler(config.config_filename),
                                        prompt="Config path",
                                        prompt_required=True,
                                        callback=default_styler.style_callback),
):
    """Initialize a new config file"""

    config['auth']['user'].set(username)
    config['auth']['password'].set(password)
    config['server']['host'].set(host)
    config['server']['port'].set(port)


@config_app.command()
def view():
    """Initialize a new config file"""
    typer.echo(config.view())
