import functools

import click
from rich import box
from rich.console import Console
from rich.table import Table

from habr.career.utils import ResponseError


def show_table(
        rows: list,
        headers: list[str] | None = None,
        console: Console | None = None,
        **kwargs
) -> None:
    table = Table(
        box=box.HORIZONTALS,
        pad_edge=False,
        show_header=bool(headers),
        **kwargs
    )

    headers = headers or []
    for header in headers:
        table.add_column(header=header)

    for row in rows:
        table.add_row(*row, style="bright_green")

    console = console or Console()
    console.clear()

    console.print(table)


def process_response_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ResponseError as e:
            error(e.get_reason())
            exit(1)
    return wrapper


def success(message: str) -> None:
    """
    Print success message.

    :param message: Text message
    :return:
    """
    click.secho(message, fg="green")


def error(message: str) -> None:
    """
    Print error message.

    :param message: Text message
    :return:
    """
    click.secho(message, err=True, fg="red")


def info(message: str) -> None:
    """
    Print informational message.x

    :param message: Text message
    :return:
    """
    click.secho(message, fg="blue")
