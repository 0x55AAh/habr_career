import click
from rich.console import Console

from habr.career.cli.config import SPINNER, EXPERT_MARK
from habr.career.cli.utils import (
    process_response_error,
    show_table,
    output_as_json,
)
from habr.career.client import HABRCareerClient
from habr.career.utils import Pagination, ConcurrentJobs


@click.group("friendships")
def cli():
    """Friendships chapter."""


@cli.group("requests")
def requests():
    """Performs operations on friendship requests."""


@cli.command("list")
@click.option(
    "-p", "--page",
    type=int,
    default=Pagination.INIT_PAGE,
    show_default=True,
    help="",
)
@click.option(
    "--json/--no-json", "as_json",
    default=False,
    show_default=True,
    help="",
)
@click.pass_obj
@process_response_error
def get_friends(
        client: HABRCareerClient,
        page: int,
        as_json: bool,
) -> None:
    """Get friends list."""
    console = Console()
    jobs = ConcurrentJobs()

    with console.status("Loading...", spinner=SPINNER):
        friends, profile = (
            jobs
            .register(client.get_friends, page)
            .register(lambda: client.profile)
            .run()
        )

    if as_json:
        console.print(
            output_as_json(
                friends=friends,
                me=profile,
            )
        )
        return

    friends_count = profile["user"]["friends"]["total"]

    # No friends
    if not friends_count:
        console.print("[blue]No friends.[/blue]")
        return

    rows = []
    for friend in friends.list_:
        is_expert = friend.is_expert
        full_name = friend.title
        if is_expert:
            full_name += f" {EXPERT_MARK}"
        username = friend.id
        subtitle = friend.subtitle
        rows.append([full_name, username, subtitle])

    show_table(
        console=console,
        title=f"Friends ({friends_count})",
        rows=rows,
        caption=", ".join([
            f"{k.title().replace("_", " ")}: {v}"
            for k, v in friends.meta.model_dump().items()
        ]),
    )


@requests.command("list")
@click.option(
    "-p", "--page",
    type=int,
    default=Pagination.INIT_PAGE,
    show_default=True,
    help="",
)
@click.option(
    "--json/--no-json", "as_json",
    default=False,
    show_default=True,
    help="",
)
@click.pass_obj
@process_response_error
def get_friendship_requests(
        client: HABRCareerClient,
        page: int,
        as_json: bool,
) -> None:
    """Get friendship requests."""
    console = Console()
    jobs = ConcurrentJobs()

    with console.status("Loading...", spinner=SPINNER):
        req, me = (
            jobs
            .register(client.get_friendship_requests, page)
            .register(lambda: client.user)
            .run()
        )

    if as_json:
        console.print(
            output_as_json(
                requests=req,
                me=me,
            )
        )
        return

    requests_count = me.user.notification_counters.friends

    # No requests
    if not requests_count:
        console.print("[blue]No requests.[/blue]")
        return

    rows = []
    for friend in req.list_:
        is_expert = friend.is_expert
        full_name = friend.title
        if is_expert:
            full_name += f" {EXPERT_MARK}"
        username = friend.id
        subtitle = friend.subtitle
        rows.append([full_name, username, subtitle])

    show_table(
        console=console,
        title=f"Requests ({requests_count})",
        rows=rows,
        caption=", ".join([
            f"{k.title().replace("_", " ")}: {v}"
            for k, v in req.meta.model_dump().items()
        ]),
    )


@requests.command("approve")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.pass_obj
@process_response_error
def approve_friend(client: HABRCareerClient, username: str) -> None:
    """Approve friendship request."""
    console = Console()
    with console.status("Approving...", spinner=SPINNER):
        client.approve_friend(username)


@requests.command("reject")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.pass_obj
@process_response_error
def reject_friend(client: HABRCareerClient, username: str) -> None:
    """Reject friendship request."""
    console = Console()
    with console.status("Rejecting...", spinner=SPINNER):
        client.reject_friend(username)


@cli.command("invite")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.pass_obj
@process_response_error
def request_new_friendship(client: HABRCareerClient, username: str) -> None:
    """Request for a new friendship to be established."""
    console = Console()
    with console.status("Inviting...", spinner=SPINNER):
        client.request_new_friendship(username)


@cli.command("cancel")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.pass_obj
@process_response_error
def cancel_pending_friendship(client: HABRCareerClient, username: str) -> None:
    """Request for pending friendship to be canceled."""
    console = Console()
    with console.status("Cancelling...", spinner=SPINNER):
        client.cancel_pending_friendship(username)


@cli.command("delete")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.pass_obj
@process_response_error
def delete_friend(client: HABRCareerClient, username: str) -> None:
    """Request for friendship to be deleted."""
    console = Console()
    with console.status("Deleting...", spinner=SPINNER):
        client.delete_friend(username)
