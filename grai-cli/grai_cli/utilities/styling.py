import typer
from typing import Callable
from rich.theme import Theme

custom_theme = Theme({"info": "#BFD2EB", "warning": "magenta", "danger": "bold red"})


def prompt_styler(*args, **kwargs) -> Callable:
    def inner(inp: str) -> str:
        return typer.style(inp, *args, **kwargs)

    strips = inner("test_value").split("test_value")
    slicer = slice(len(strips[0]), -len(strips[1]))

    def style_inversion(inp: str) -> str:
        if inp.startswith(strips[0]):
            return inp[slicer]
        return inp

    inner.style_callback = style_inversion
    return inner


def strip_styling(styler: prompt_styler) -> Callable:
    def inner(fn: Callable) -> Callable:
        def inner2(inp: str) -> str:
            return fn(styler.style_callback(inp))

        return inner2

    return inner


# command_styler = prompt_styler(fg="BFD2EB", bold=True)
default_styler = prompt_styler(fg=typer.colors.GREEN, bold=True)
