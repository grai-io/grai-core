import typer
from pydantic import AnyHttpUrl, BaseModel, EmailStr

from grai_cli.utilities.styling import default_styler, strip_style

default_style_stripper = strip_style(default_styler)


class UrlModel(BaseModel):
    url: AnyHttpUrl


def url_callback(styled_input: str) -> str:
    """

    Args:
        styled_input: The potentially styled input from the user

    Returns:
        a valid url
    Raises:

    """
    input = typer.unstyle(styled_input)
    try:
        UrlModel(url=input)
    except:
        raise typer.BadParameter(
            f"`{input}` is not a valid url. Please insure your address includes the scheme (http:// or https://)"
        )

    return input


class EmailModel(BaseModel):
    email: EmailStr


def username_callback(styled_input: str) -> str:
    """

    Args:
        styled_input: The potentially styled input from the user

    Returns:
        a valid email address
    Raises:

    """
    input = typer.unstyle(styled_input)
    try:
        EmailModel(email=input)
    except:
        raise typer.BadParameter(f"`{input}` is not a valid email address.")

    return input


def workspace_callback(styled_input: str) -> str:
    """

    Args:
        styled_input: The potentially styled input from the user

    Returns:
        a valid workspace string
    Raises:

    """
    input = typer.unstyle(styled_input)
    if len(input) == 0:
        raise typer.BadParameter("Workspace is empty")
    return input


def password_callback(styled_input: str) -> str:
    """

    Args:
        styled_input: The potentially styled input from the user

    Returns:
        a valida password string
    Raises:

    """

    input = typer.unstyle(styled_input)
    if len(input) == 0:
        raise typer.BadParameter("Password cannot be empty")
    return input


def api_key_callback(styled_input: str) -> str:
    """ """
    input = typer.unstyle(styled_input)
    if len(input) == 0:
        raise typer.BadParameter(
            "Api Key ought to look like {prefix}.{id} where prefix is 8 characters long and id is 32 characters long."
        )
    return input
