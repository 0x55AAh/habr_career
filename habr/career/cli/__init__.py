from typing import cast

import click
from click import Command
from rich.console import Console

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
from .utils import error, info, process_response_error


@click.group()
@click.option(
    "--token",
    envvar="HABR_CAREER_TOKEN",
    hidden=True,
)
@click.option(
    "--session-id",
    envvar="HABR_CAREER_SESSION_ID",
    hidden=True,
)
@click.option(
    "--debug/--no-debug",
    envvar="HABR_CAREER_DEBUG",
    default=False,
    hidden=True,
)
@click.version_option(__version__, message="Version: %(version)s")
@click.pass_context
def main(ctx, token: str, session_id, debug: bool) -> None:
    """Habr Career console application."""
    ctx.obj = HABRCareerClient(
        auth=TokenAuthenticator(token=token),
        session_id=session_id,
        debug=debug,
    )


@main.command("logout")
@click.pass_obj
@process_response_error
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


main.add_command(cast(Command, companies.cli))
main.add_command(cast(Command, conversations.cli))
# main.add_command(cast(Command, courses.cli))
# main.add_command(cast(Command, experts.cli))
main.add_command(cast(Command, friendships.cli))
# main.add_command(cast(Command, resumes.cli))
main.add_command(cast(Command, salaries.cli))
main.add_command(cast(Command, users.cli))
# main.add_command(cast(Command, vacancies.cli))
