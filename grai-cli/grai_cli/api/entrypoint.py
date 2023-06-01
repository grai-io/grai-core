from typing import Optional

import click
import typer

from grai_cli.utilities.telemetry import Telemetry
from grai_cli.utilities.utilities import HAS_RICH, default_callback


def result_callback(*args, **kwargs):
    """

    Args:
        *args:
        **kwargs:

    Returns:

    Raises:

    """
    ctx = click.get_current_context()
    command_path = ctx.meta["command_path"]
    if command_path and command_path[0] != "telemetry":
        command = f"grai {' '.join(command_path)}"
        Telemetry.capture(command)


app = typer.Typer(
    rich_markup_mode="rich" if HAS_RICH else None,
    invoke_without_command=True,
    no_args_is_help=True,
    help="Grai CLI",
    pretty_exceptions_show_locals=False,
    result_callback=result_callback,
)


@app.callback()
def callback(
    ctx: typer.Context,
    telemetry: Optional[bool] = typer.Option(None, show_default=False, help="Enable or disable telemetry"),
):
    """Grai CLI

    Args:
        ctx (typer.Context):
        telemetry (Optional[bool], optional):  (Default value = typer.Option(None, show_default=False, help="Enable or disable telemetry"))

    Returns:

    Raises:

    """

    if telemetry is not None:
        from grai_cli.settings.cache import cache

        cache.set("telemetry_consent", telemetry)

    default_callback(ctx)
