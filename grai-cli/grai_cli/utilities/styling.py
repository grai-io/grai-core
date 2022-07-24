from typing import Callable

import typer
from rich.theme import Theme


class GraiColors:
    mango = (255, 181, 103)
    polo = (191, 210, 235)
    kobi = (241, 215, 224)
    bastille = (53, 29, 54)
    soapstone = (255, 255, 255)


custom_theme = Theme({"info": "#BFD2EB", "warning": "#ff0000", "danger": "bold red"})


def prompt_styler(*args, **kwargs) -> Callable[[str], str]:
    def inner(inp: str) -> str:
        return typer.style(inp, *args, **kwargs)

    return inner


def strip_style(fn: Callable[[str], str]) -> Callable[[str], str]:
    def inner(inp: str) -> str:
        return fn(typer.unstyle(inp))

    return inner


default_styler = prompt_styler(fg=GraiColors.mango, bold=True)
