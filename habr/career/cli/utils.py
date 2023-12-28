import functools
import unicodedata

import click
from rich import box
from rich.box import Box
from rich.console import Console
from rich.table import Table

from habr.career.utils import ResponseError, cleanup_tags, NotAuthorizedError


def truncate_chars(text: str, length: int) -> str:
    text = text.replace("\n", " ")
    text = cleanup_tags(text, br_replace=False).strip()
    if len(text) <= length:
        return text
    else:
        text = text[:length]
        d = str_display_width(text) - length
        text = text[:length - d]
        return f"{text}..."


def str_display_width(text: str) -> int:
    def get_char_display_width(unicode_char):
        match unicodedata.east_asian_width(unicode_char):
            case "W": return 2
            case _: return 1
    return sum(map(get_char_display_width, text))


def build_table(
        rows: list,
        headers: list[str] | None = None,
        box_: Box | None = box.HORIZONTALS,
        **kwargs
) -> Table:
    table = Table(
        box=box_,
        pad_edge=False,
        show_header=bool(headers),
        **kwargs
    )

    headers = headers or []
    for header in headers:
        table.add_column(header=header)

    for row in rows:
        table.add_row(*row, style="bright_green")

    return table


def show_table(
        rows: list,
        headers: list[str] | None = None,
        console: Console | None = None,
        **kwargs
) -> None:
    table = build_table(rows=rows, headers=headers, **kwargs)

    console = console or Console()
    console.clear()

    console.print(table)


def process_response_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ResponseError as e:
            error(e.get_reason(), exit_code=1)
        except NotAuthorizedError:
            error(
                "Not authorized. Please login.",
                exit_code=1
            )
    return wrapper


def success(message: str) -> None:
    """
    Print success message.

    :param message: Text message
    :return:
    """
    click.secho(message, fg="green")


def error(message: str, exit_code: int | None = None) -> None:
    """
    Print error message.

    :param message: Text message
    :param exit_code: Exit code
    :return:
    """
    click.secho(message, err=True, fg="red")
    if exit_code is not None:
        exit(exit_code)


def info(message: str) -> None:
    """
    Print informational message.x

    :param message: Text message
    :return:
    """
    click.secho(message, fg="blue")
