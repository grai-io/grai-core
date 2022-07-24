import typer

app = typer.Typer(rich_markup_mode="rich", no_args_is_help=True, help="Grai CLI")


@app.callback()
def callback():
    """
    Grai CLI
    """
