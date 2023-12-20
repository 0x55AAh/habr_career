import itertools

import click
from rich.align import Align

from habr.career.cli.config import SPINNER
from habr.career.cli.utils import process_response_error, show_table
from habr.career.client import HABRCareerClient
from habr.career.utils import (
    ComplainReason,
    cleanup_tags,
    ConcurrentJobs, Pagination,
)

from rich.console import Console
from rich.text import Text


def truncate_chars(text: str, length: int) -> str:
    text = text.replace("\n", " ")
    text = cleanup_tags(text).strip()
    if len(text) <= length:
        return text
    else:
        text = text[:length].rstrip(".")
        return f"{text}..."


def multiline_prompt(text: str = "", *args, **kwargs) -> str:
    lines = []
    while True:
        line = click.prompt(text, *args, **kwargs)
        if line:
            lines.append(line)
        else:
            break
    return "\n".join(lines)


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
def get_conversations(client: HABRCareerClient,
                      search: str, page: int) -> None:
    """Get conversations list."""
    console = Console()

    with console.status("Loading...", spinner=SPINNER):
        conversations = client.get_conversations(search, page)

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
            prefix = "[blue]Me: [/blue]" if is_mine else ""
            body = f"{prefix}{body}"
            c = len(prefix) - 4 if prefix else 0
            body = truncate_chars(body, length=40 + c)

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
            full_name += f" \U0001F393"

        username = f"{style}{username}"
        created_at = f"{style}{created_at}"
        body = f"{style}{body}"

        rows.append([full_name, username, created_at, body])

    total_count = conversations.meta.total_count
    title = "Conversations"
    if total_count:
        title = f"{title} ({total_count})"

    # TODO: No conversations

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

    theme = conversation.theme
    is_banned = conversation.banned.status
    banned_message = conversation.banned.message
    has_new_message = conversation.has_new_message
    other_name = other["user"]["title"]
    messages = conversation.messages.data

    message_width = 60
    table_width = 80

    captions = []
    if is_banned:
        captions.append(f"[red]{banned_message}[/red]")

    rows = []
    if not messages:
        rows.append(["No messages. Write your first message."])  # TODO
    else:
        captions.append(", ".join([
            f"{k.title().replace("_", " ")}: {v}"
            for k, v in conversation.messages.meta.model_dump().items()
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
def send_message(client: HABRCareerClient,
                 username: str,
                 message: str | None,
                 template_id: int | None) -> None:
    """Send message to specified user."""
    console = Console()
    with console.status("Sending...", spinner=SPINNER):
        if message is None and template_id is not None:
            result = client.get_templates()
            templates = {t.id: t for t in result.templates}
            template = templates[template_id]  # TODO
            message = template.body
        if message is None:
            message = multiline_prompt()
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
    with console.status("Un-reading...", spinner=SPINNER):
        # TODO: if the last message is mine, disallow operation
        #       result = client.get_messages(username, page)
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
def change_conversation_subject(client: HABRCareerClient,
                                username: str, subject: str) -> None:
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
def complain_conversation(client: HABRCareerClient,
                          username: str, reason: ComplainReason) -> None:
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
def update_template(client: HABRCareerClient,
                    id_: int, title: str, body: str) -> None:
    """Update template with specified attributes."""
    console = Console()
    with console.status("Updating...", spinner=SPINNER):
        client.update_template(id_, title=title, body=body)
