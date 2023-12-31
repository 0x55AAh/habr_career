import itertools

import click
from rich.align import Align

from habr.career.cli.config import SPINNER, EXPERT_MARK
from habr.career.cli.utils import (
    process_response_error,
    show_table,
    truncate_chars,
)
from habr.career.client import HABRCareerClient
from habr.career.utils import (
    ComplainReason,
    cleanup_tags,
    ConcurrentJobs, Pagination,
)

from rich.console import Console
from rich.text import Text


@click.group("conversations")
def cli() -> None:
    """Conversations chapter."""


@cli.group("templates")
def templates() -> None:
    """Performs message template operations."""


@cli.command("list")
@click.option(
    "-q", "--search",
    help="",
)
@click.option(
    "-p", "--page",
    type=int,
    default=Pagination.INIT_PAGE,
    show_default=True,
    help="",
)
@click.pass_obj
@process_response_error
def get_conversations(
        client: HABRCareerClient,
        search: str,
        page: int,
) -> None:
    """Get conversations list."""
    console = Console()

    with console.status("Loading...", spinner=SPINNER):
        conversations = client.get_conversations(search, page)

    total_count = conversations.meta.total_count

    # No conversations
    if not total_count:
        console.print("[blue]No conversations[/blue]")
        return

    rows = []
    for username, con in conversations.objects.items():
        last_message = con.conversation.last_message

        # Get last message `is_mine` field
        is_mine = getattr(last_message, "is_mine", None)
        # Get last message `is_read` field
        is_read = getattr(last_message, "is_read", None)

        # Get banned status
        is_banned = con.banned.status
        banned_message = con.banned.message

        # Get last message `body` field
        body = getattr(last_message, "body", banned_message)
        if body:
            prefix = "Me: " if is_mine else ""
            body = truncate_chars(f"{prefix}{body}", length=40)
            body = f"[blue]{prefix}[/blue]" + body[len(prefix):]

        # Get last message `created_at` field
        created_at = getattr(last_message, "created_at", None)
        if created_at:
            # import locale
            # locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
            created_at = created_at.strftime("%d %b %Y")
        else:
            created_at = ""

        style = ""
        if not is_banned and (is_mine or is_read):
            style = "[dim]"
        elif is_banned:
            style = "[dim bright_red]"

        full_name = f"{style}{con.full_name}"
        if con.is_expert:
            full_name += f" {EXPERT_MARK}"

        username = f"{style}{username}"
        created_at = f"{style}{created_at}"
        body = f"{style}{body}"

        rows.append([full_name, username, created_at, body])

    title = "Conversations"
    if total_count:
        title = f"{title} ({total_count})"

    show_table(
        console=console,
        title=title,
        rows=rows,
        caption=", ".join([
            f"{k.title().replace("_", " ")}: {v}"
            for k, v in conversations.meta.model_dump(
                exclude={"total_count"}, exclude_unset=True).items()
        ]),
    )


@cli.command("connect")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.option(
    "-p", "--page",
    type=int,
    default=Pagination.INIT_PAGE,
    show_default=True,
    help="",
)
@click.pass_obj
@process_response_error
def connect(client: HABRCareerClient, username: str, page: int) -> None:
    """Get or create conversation with a specified user."""
    console = Console()
    jobs = ConcurrentJobs()

    with console.status("Loading...", spinner=SPINNER):
        conversation, me, other, data = (
            jobs
            .register(client.connect, username, page)
            .register(lambda: client.user)
            .register(client.get_profile, username)
            .register(client.get_conversation_data, username)
            .run()
        )

    messages = conversation.messages.data
    meta = conversation.messages.meta

    # No messages
    if not meta.total:
        console.print(
            "[blue]No messages. Write your first message.[/blue]")
        return

    theme = conversation.theme
    is_banned = conversation.banned.status
    banned_message = conversation.banned.message
    has_new_message = conversation.has_new_message
    other_name = other["user"]["title"]

    message_width = 60
    table_width = 80

    captions = []
    if is_banned:
        captions.append(f"[red]{banned_message}[/red]")

    rows = []
    captions.append(", ".join([
        f"{k.title().replace("_", " ")}: {v}"
        for k, v in meta.model_dump().items()
    ]))

    for date, messages_ in itertools.groupby(
            messages, key=lambda m: m.created_at.date()):
        date = date.strftime("%d %B %Y")
        rows.append(
            [Text(date, justify="center", style="blue", end="\n\n")])
        for message in messages_:
            body = cleanup_tags(message.body, strip=True, separator="\n")
            if message.is_mine:
                author = me.user.full_name
                # author = "Me"
            else:
                author = other_name
            time = message.created_at.strftime("%H:%M")
            author = (f"[blue bold]{author}[/blue bold]"
                      f" [bright_black]{time}[/bright_black]")
            body = Align(
                f"{author}\n{body}\n",
                align="right" if message.is_mine else "left",
                width=message_width,
            )
            rows.append([body])

    titles = [other_name, data["interlocutor"]["subtitle"]]

    show_table(
        console=console,
        title="\n".join([t for t in titles if t]),
        rows=rows,
        caption="\n".join(captions),
        width=table_width,
    )


@cli.command("disconnect")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.pass_obj
@process_response_error
def disconnect(client: HABRCareerClient, username: str) -> None:
    """Remove conversation with specified user."""
    console = Console()
    with console.status("Disconnecting...", spinner=SPINNER):
        client.disconnect(username)


@cli.command("send")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.option(
    "-m", "--message",
    help="",
)
@click.option(
    "-t", "--template-id", "template_id",
    help="",
)
@click.pass_obj
@process_response_error
def send_message(
        client: HABRCareerClient,
        username: str,
        message: str | None,
        template_id: int | None,
) -> None:
    """Send message to specified user."""
    from habr.career.client.conversations.models import Template

    def get_template(id_: int) -> Template:
        res = client.get_templates()
        templates_list = {t.id: t for t in res.templates}
        try:
            return templates_list[id_]
        except KeyError:
            console.print("[red]No template found.[/red]")
            exit(1)

    console = Console()

    with console.status("Sending...", spinner=SPINNER):
        if message is None and template_id is not None:
            message = get_template(template_id).body
        if message is None:
            message = click.prompt("Your message")
        client.send_message(username, message)


@cli.command("unread")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.pass_obj
@process_response_error
def unread_conversation(client: HABRCareerClient, username: str) -> None:
    """Mark conversation with a specified user as unread."""
    console = Console()
    with console.status("Making unread...", spinner=SPINNER):
        result = client.get_messages(username, page=1)
        last_message_is_mine = result.data[-1].is_mine
        if last_message_is_mine:
            console.print("[red]Operation is not allowed:[/red]")
            console.print("[red]\\_ The last message is mine.[/red]")
            exit(1)
        client.unread_conversation(username)


@cli.command("change_subject")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.option(
    "-s", "--subject",
    required=True,
    help="",
)
@click.pass_obj
@process_response_error
def change_conversation_subject(
        client: HABRCareerClient,
        username: str,
        subject: str,
) -> None:
    """Change a specified user conversation topic."""
    console = Console()
    with console.status("Changing...", spinner=SPINNER):
        client.change_conversation_subject(username, subject)


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
def complain_conversation(
        client: HABRCareerClient,
        username: str,
        reason: ComplainReason,
) -> None:
    """Complain to a specified user."""
    console = Console()
    with console.status("Complaining...", spinner=SPINNER):
        client.complain_conversation(username, reason)


@templates.command("list")
@click.pass_obj
@process_response_error
def get_templates(client: HABRCareerClient) -> None:
    """Get all created templates."""
    console = Console()

    with console.status("Loading...", spinner=SPINNER):
        result = client.get_templates()

    show_table(
        console=console,
        title=f"Templates ({len(result.templates)})",
        rows=[
            [
                str(template.id),
                template.title,
                template.body,
            ] for template in result.templates
        ],
        width=100,
    )


@templates.command("create")
@click.option(
    "-t", "--title",
    required=True,
    help="",
)
@click.option(
    "-b", "--body",
    required=True,
    help="",
)
@click.pass_obj
@process_response_error
def create_template(client: HABRCareerClient, title: str, body: str) -> None:
    """Create new template with specified attributes."""
    console = Console()
    with console.status("Creating...", spinner=SPINNER):
        client.create_template(title=title, body=body)


@templates.command("delete")
@click.option(
    "-i", "--id", "id_",
    type=int,
    required=True,
    help="",
)
@click.pass_obj
@process_response_error
def delete_template(client: HABRCareerClient, id_: int) -> None:
    """Remove template."""
    console = Console()
    with console.status("Deleting...", spinner=SPINNER):
        client.delete_template(id_)


@templates.command("update")
@click.option(
    "-i", "--id", "id_",
    type=int,
    required=True,
    help="",
)
@click.option(
    "-t", "--title",
    help="",
)
@click.option(
    "-b", "--body",
    help="",
)
@click.pass_obj
@process_response_error
def update_template(
        client: HABRCareerClient,
        id_: int,
        title: str,
        body: str,
) -> None:
    """Update template with specified attributes."""
    console = Console()
    with console.status("Updating...", spinner=SPINNER):
        client.update_template(id_, title=title, body=body)
