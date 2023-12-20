import os

import click
from rich.console import Console

from habr.career.cli.config import SPINNER
from habr.career.cli.utils import process_response_error
from habr.career.client import HABRCareerClient
from habr.career.client.users import CVFormat
from habr.career.utils import ComplainReason


@click.group("users")
def cli():
    """Users chapter."""


@cli.command("profile")
@click.option(
    "-u", "--username",
    help="",
)
@click.pass_obj
@process_response_error
def get_profile(client: HABRCareerClient, username: str | None) -> None:
    """Get arbitrary user profile data."""
    console = Console()
    with console.status("Loading...", spinner=SPINNER):
        username = username or client.username
        result = client.get_profile(username)
    # TODO: show data


@cli.command("cv")
@click.option(
    "-u", "--username",
    help="",
)
@click.option(
    "-f", "--format", "fmt",
    type=click.Choice(CVFormat),
    default=CVFormat.PDF,
    show_default=True,
    help="",
)
@click.option(
    "-p", "--path",
    required=True,
    help="",
)
@click.pass_obj
@process_response_error
def get_cv(
        client: HABRCareerClient,
        username: str | None,
        fmt: CVFormat,
        path: str,
) -> None:
    """Get CV for the requested user."""
    console = Console()

    with console.status("Loading...", spinner=SPINNER):
        username = username or client.username
        data = client.get_cv(username, fmt)

    path = os.path.abspath(path)
    try:
        os.makedirs(os.path.dirname(path))
    except FileExistsError:
        pass

    with open(path, "wb") as f:
        f.write(data)


@cli.command("complain")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.option(
    "-r", "--reason",
    type=click.Choice(ComplainReason),
    required=True,
    help="",
)
@click.pass_obj
@process_response_error
def complain_on_user(
        client: HABRCareerClient,
        username: str,
        reason: ComplainReason,
) -> None:
    """Complain on user."""
    console = Console()
    with console.status("Complaining...", spinner=SPINNER):
        client.complain_on_user(username, reason)
