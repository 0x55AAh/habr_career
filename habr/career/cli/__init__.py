import click
from click import Command
from rich.console import Console
from typing import cast

from habr.career import __version__
from habr.career.client import HABRCareerClient, TokenAuthenticator
from habr.career.utils import LogoutError
from .commands import (
    companies,
    conversations,
    courses,
    experts,
    friendships,
    resumes,
    salaries,
    users,
    vacancies,
)
from .config import SPINNER
from .utils import error, info


@click.group()
@click.option(
    "--token",
    envvar="HABR_CAREER_TOKEN",
    help="Auth token.",
)
@click.pass_context
def main(ctx, token: str) -> None:
    """Habr Career console application."""
    ctx.obj = HABRCareerClient(auth=TokenAuthenticator(token=token))


@main.command("logout")
@click.pass_obj
def logout(client: HABRCareerClient) -> None:
    """Perform logout operation to invalidate auth token."""
    console = Console()
    try:
        with console.status("Logging out...", spinner=SPINNER):
            client.logout()
    except LogoutError as e:
        error(f"Logging out failed.")
        error(f"\\_ Reason: {e}")
        exit(1)


@main.command("version")
def version() -> None:
    """Show client version and exit."""
    info(f"Current version: {__version__}")


main.add_command(cast(Command, companies.cli))
main.add_command(cast(Command, conversations.cli))
main.add_command(cast(Command, courses.cli))
main.add_command(cast(Command, experts.cli))
main.add_command(cast(Command, friendships.cli))
main.add_command(cast(Command, resumes.cli))
main.add_command(cast(Command, salaries.cli))
main.add_command(cast(Command, users.cli))
main.add_command(cast(Command, vacancies.cli))
