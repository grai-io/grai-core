import typer

app = typer.Typer(rich_markup_mode="rich", no_args_is_help=True, help="Grai CLI")


def check_for_config_file():
    import grai_cli
    import subprocess
    from grai_cli.settings.cache import cache

    if grai_cli.config.has_configfile or cache.has_init:
        return

    message = f"No config file found in ({grai_cli.config.config_filename}). Would you like to create one now?"
    if not typer.confirm(message):
        cache.set('has_init',  True)
        return

    cache.set('has_init', True)
    subprocess.run(["grai", "config", "init"])


@app.callback()
def callback():
    """
    Grai CLI
    """
    check_for_config_file()

