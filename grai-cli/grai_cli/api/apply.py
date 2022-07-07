import typer
from pathlib import Path
from grai_cli.api.entrypoint import app
from grai_cli.settings.schemas.schema_resolver import validate_file


@app.command('apply')
def apply(file: Path = typer.Argument(...)):
    result = validate_file(file)
    print(result)

