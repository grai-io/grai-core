import typer

from grai_cli.utilities.styling import default_styler, strip_style

default_style_stripper = strip_style(default_styler)


def username_callback(inp: str):
    if len(inp) == 0:
        raise typer.BadParameter("Password is invalid for <reasons>")
    return inp


def password_callback(inp: str):
    def password_is_valid(inp: str):
        # TODO
        return True

    if not password_is_valid(inp):
        # TODO
        raise typer.BadParameter("Password is invalid for <reasons>")
    return inp


def host_callback(inp: str):
    def host_is_valid(inp: str):
        # TODO
        return True

    if not host_is_valid(inp):
        raise typer.BadParameter(f"Invalid hostname {inp}")
    return inp


def port_callback(inp: str):
    error = typer.BadParameter(
        f"'{inp}' is not a valid port, should be a number between 1 and 65535"
    )
    if not inp.isnumeric():
        raise error
    else:
        int_inp = int(inp)
        if 1 > int_inp < 65535:
            raise error

    return str(int_inp)
