#!/usr/bin/env python3
"""Test"""
import click

from habr.career import HABRCareerClient, TokenAuthenticator
from habr.career.utils import ComplainReason, LogoutError


@click.group(help=__doc__)
@click.option("--token", envvar="HABR_CAREER_TOKEN")
@click.pass_context
def cli(ctx, token: str):
    ctx.obj = HABRCareerClient(auth=TokenAuthenticator(token=token))


# +++++++++++++++++++++++++++++ Chapters List +++++++++++++++++++++++++++++

@cli.group()
def conversations():
    """Conversations chapter."""


@cli.group()
def users():
    """Users chapter."""


# +++++++++++++++++++++++++ Conversations Commands ++++++++++++++++++++++++

@conversations.command("get_conversations")
@click.option(
    "-q", "--search",
    required=True,
    help="",
)
@click.option(
    "-p", "--page",
    type=int,
    default=1,
    show_default=True,
    help="",
)
@click.pass_obj
def get_conversations(client: HABRCareerClient, search: str, page: int):
    result = client.get_conversations(search, page)
    # TODO


@conversations.command("connect")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.pass_obj
def connect(client: HABRCareerClient, username: str):
    result = client.connect(username)
    # TODO


@conversations.command("disconnect")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.pass_obj
def disconnect(client: HABRCareerClient, username: str):
    result = client.disconnect(username)
    # TODO


@conversations.command("get_messages")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.pass_obj
def get_messages(client: HABRCareerClient, username: str):
    result = client.get_messages(username)
    # TODO


@conversations.command("send_message")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.option(
    "-m", "--message",
    required=True,
    help="",
)
@click.pass_obj
def send_message(client: HABRCareerClient, username: str, massage: str):
    result = client.send_message(username, massage)
    # TODO


@conversations.command("unread_conversation")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.pass_obj
def unread_conversation(client: HABRCareerClient, username: str):
    result = client.unread_conversation(username)
    # TODO


@conversations.command("change_conversation_subject")
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
def change_conversation_subject(client: HABRCareerClient,
                                username: str, subject: str):
    result = client.change_conversation_subject(username, subject)
    # TODO


@conversations.command("complain_conversation")
@click.option(
    "-u", "--username",
    required=True,
    help="",
)
@click.option(
    "-r", "--reason",
    type=click.Choice(ComplainReason),
    case_sensitive=False,
    required=True,
    help="",
)
@click.pass_obj
def complain_conversation(client: HABRCareerClient,
                          username: str, reason: ComplainReason):
    result = client.complain_conversation(username, reason)
    # TODO


@conversations.command("get_templates")
@click.pass_obj
def get_templates(client: HABRCareerClient):
    result = client.get_templates()
    # TODO


@conversations.command("create_template")
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
def create_template(client: HABRCareerClient, title: str, body: str):
    result = client.create_template(title=title, body=body)
    # TODO


@conversations.command("delete_template")
@click.option(
    "-i", "--id", "id_",
    type=int,
    required=True,
    help="",
)
@click.pass_obj
def delete_template(client: HABRCareerClient, id_: int):
    result = client.delete_template(id_)
    # TODO


@conversations.command("update_template")
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
def update_template(client: HABRCareerClient,
                    id_: int, title: str, body: str):
    result = client.update_template(id_, title=title, body=body)
    # TODO


# +++++++++++++++++++++++++++ General Commands ++++++++++++++++++++++++++++

@cli.command("logout")
@click.pass_obj
def logout(client: HABRCareerClient):
    """Perform logout operation to invalidate auth token."""
    try:
        client.logout()
    except LogoutError:
        # TODO
        pass


if __name__ == "__main__":
    cli()
