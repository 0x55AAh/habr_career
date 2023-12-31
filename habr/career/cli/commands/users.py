import os

import click
from rich import box
from rich.console import Console

from habr.career.cli.config import SPINNER, EXPERT_MARK
from habr.career.cli.utils import (
    process_response_error,
    show_table,
    build_table,
)
from habr.career.client import HABRCareerClient
from habr.career.client.users import CVFormat
from habr.career.utils import (
    ComplainReason,
    cleanup_tags,
    CurrencySymbol,
)


@click.group("users")
def cli():
    """Users chapter."""


@cli.command("info")
@click.option(
    "-u", "--username",
    help="Username of requested user.",
)
@click.option(
    "--basic/--no-basic", "show_basic",
    default=True,
    show_default=True,
    help="Show basic information.",
)
@click.option(
    "--about/--no-about", "show_about",
    default=False,
    help="Show `about me` section.",
)
@click.option(
    "--companies/--no-companies", "show_companies",
    default=False,
    help="Show companies user worked for.",
)
@click.option(
    "--education/--no-education", "show_education",
    default=False,
    help="Show info related to education.",
)
@click.option(
    "--additional-education/--no-additional-education",
    "show_additional_education",
    default=False,
    help="Show info related to additional education.",
)
@click.option(
    "--expert/--no-expert", "show_expert",
    default=False,
    help="Show expert info.",
)
@click.option(
    "-a", "--all", "show_all",
    is_flag=True,
    default=False,
    help="Show all information about the user.",
)
@click.pass_obj
@process_response_error
def get_profile(
        client: HABRCareerClient,
        username: str | None,
        show_basic: bool,
        show_about: bool,
        show_companies: bool,
        show_education: bool,
        show_additional_education: bool,
        show_expert: bool,
        show_all: bool,
) -> None:
    """Get arbitrary user profile data."""
    console = Console()

    with console.status("Loading...", spinner=SPINNER):
        username = username or client.username
        result = client.get_profile(username)

    table_width = 100

    user = result["user"]
    resume = result["resume"]

    if show_basic or show_all:
        skills = [s["title"] for s in user["skills"]]
        visibility = user["visibility"]
        try:
            contacts_visibility = user["contacts"]["hint"]["title"]
        except KeyError:
            contacts_visibility = None

        specialization = user["specialization"]
        recommendations_count = user["recommendationLetters"]
        friends_count = user["friends"]

        achievements = [a["title"] for a in user["achievements"]]
        achievements_total = user["achievementsTotal"]

        contacts_table = build_table(
            rows=[
                (
                    f"[bright_black]{c["title"]}[/bright_black]",
                    c["value"]["title"],
                ) for c in user["contacts"]["items"]
            ],
            box_=box.SIMPLE,
            show_edge=False,
        )

        curated_companies_table = build_table(
            rows=[
                (f"{c["title"]} [bright_black]{c["subtitle"]}[/bright_black]",)
                for c in user["curatedCompanies"]
            ],
            box_=box.SIMPLE,
            show_edge=False,
        )

        info = [specialization and specialization["title"]]
        info += [d["title"] for d in user["divisions"]]
        info += [user["qualification"]]

        status = [user["salary"], user["availability"]]

        rows = [
            (f"Achievements ({len(achievements)}/{achievements_total})",
             " • ".join(achievements)),
            ("Age", user["age"]),
            ("Experience", user["experience"]),
            ("Registered", user["registeredAt"]),
            ("Last Visited", user["lastVisited"]),
            ("Location", user["location"]),
            ("Relocation", user["relocation"]),
            ("Skills", " • ".join(skills)),
            ("Contacts", contacts_table.rows and contacts_table),
            ("Recommendations", str(recommendations_count["total"])),
            ("Friends", str(friends_count["total"])),
            (
                "Curated Companies",
                curated_companies_table.rows and curated_companies_table
            ),
        ]

        captions = [
            contacts_visibility,
            visibility and visibility["title"],
        ]

        full_name = user["title"]
        if user["isExpert"]:
            full_name += f" {EXPERT_MARK}"

        friendship = {
            "accepted": "Friend",
            "none": "Not Friend",
            "incoming": "",
            "cancelled": "",
            "pending": "Friendship Requested",
            None: None,
        }[user["friendship"]]

        titles = [
            " • ".join(filter(lambda x: x, [
                f"{full_name} ({user["id"]})",
                friendship,
            ])),
            user["site"] and user["site"]["href"],
            " • ".join(i for i in info if i),
            " • ".join(s for s in status if s),
        ]
        show_table(
            console=console,
            title="\n".join(t for t in titles if t),
            rows=[
                (f"[bold blue]{h}[/bold blue]", v)
                for h, v in rows if v
            ],
            caption="\n".join(
                c + ("" if i < len(captions) - 1 else "\n")
                for i, c in enumerate(captions) if c
            ),
            width=table_width,
        )

    about = resume["about"]
    if (show_about or show_all) and about and about["value"]:
        show_table(
            console=console,
            title="About Me",
            rows=[(cleanup_tags(about["value"]),)],
            width=table_width,
        )

    def show_section(key1: str, key2: str, title: str = None) -> None:
        title = title or key1.title()
        data = resume.get(key1) or {}
        items = data.get("items") or []
        count = len(items)
        show_table(
            console=console,
            title=f"{title} ({count})",
            rows=[
                (
                    "\n".join(
                        f"[bright_black]{v}[/bright_black]" if i > 0
                        else f"[blue]{v}[/blue]"
                        for i, v in enumerate(
                            filter(lambda x: x, [
                                c["title"],
                                c.get("subtitle"),
                                " • ".join(filter(lambda x: x, [
                                    c.get("location"),
                                    c.get("users", {}).get("title"),
                                ])),
                            ])
                        )
                    ).strip() + ("\n" if n < count - 1 else ""),
                    "\n\n".join(
                        "\n".join(x for x in [
                            f"[blue]{p["title"]}[/blue]",
                            f"[bright_black]{p["duration"]}[/bright_black]\n",
                            p.get("tags") and f"[bright_black]{" • ".join(
                                x["title"] for x in p.get("tags", [])
                            )}[/bright_black]\n",
                            cleanup_tags(p["message"]),
                        ] if x) for p in c[key2]
                    ).strip()
                    + ("\n" if n < count - 1 else ""),
                ) for n, c in enumerate(items)
            ],
            width=table_width,
        )

    if show_companies or show_all:
        show_section(key1="companies", key2="positions")

    if show_education or show_all:
        show_section(key1="education", key2="courses")

    if show_additional_education or show_all:
        show_section(
            key1="additionalEducation",
            key2="courses",
            title="Additional Education",
        )

    expert = resume["habr_expert"]
    if (show_expert or show_all) and expert:
        score = expert["score"]
        requests = expert["requests"]
        description = expert["description"]
        qualifications = [x["title"] for x in expert["qualifications"]]
        specializations = [x["title"] for x in expert["specializations"]]
        skills = [x["title"] for x in expert["skills"]]

        rate = expert["rate"]
        price = rate["amount"]
        currency = rate["currency"]
        free_intro = rate["freeIntro"]

        titles = [
            "Expert",
            f"Connections: {score["connections"]}",
            price and " • ".join(x for x in [
                price and f"{price} {CurrencySymbol.by_name(currency)}/hour",
                free_intro and "Free intro"
            ] if x),
        ]

        requests_table = build_table(
            rows=[
                (
                    f"[bright_black]{x["title"]}[/bright_black]",
                    " • ".join(i["title"] for i in x["items"]),
                ) for x in requests
            ],
            box_=box.SIMPLE,
            show_edge=False,
        )

        rows = [
            ("Description", description and cleanup_tags(description)),
            ("Qualifications", " • ".join(qualifications)),
            ("Specializations", " • ".join(specializations)),
            ("Skills", " • ".join(skills)),
            ("Requests", requests_table),
        ]

        show_table(
            console=console,
            title="\n".join([x for x in titles if x]),
            rows=[(f"[bold blue]{h}[/bold blue]", v) for h, v in rows if v],
            width=table_width,
        )

    # TODO
    #  recommendation_letters = resume["recommendationLetters"]


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
    "-o", "--output",
    type=click.Path(writable=True, resolve_path=True, dir_okay=False),
    required=True,
    help="",
)
@click.pass_obj
@process_response_error
def get_cv(
        client: HABRCareerClient,
        username: str | None,
        fmt: CVFormat,
        output: str,
) -> None:
    """Get CV for the requested user."""
    console = Console()

    with console.status("Downloading...", spinner=SPINNER):
        username = username or client.username
        data = client.get_cv(username, fmt)

    # try:
    #     os.makedirs(os.path.dirname(path))
    # except FileExistsError:
    #     pass

    with click.open_file(output, "wb") as f:
        f.write(data)

    click.echo(f"File saved to {click.format_filename(output)}")


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
