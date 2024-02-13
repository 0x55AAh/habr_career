from datetime import datetime

import click
from rich import box
from rich.console import Console
from rich.table import Table

from habr.career.cli.config import SPINNER
from habr.career.cli.utils import (
    process_response_error,
    show_table,
    build_table,
    output_as_json,
)
from habr.career.client import HABRCareerClient
from habr.career.client.companies import CompanySize, CompanyRatingCriteria
from habr.career.utils import Pagination, cleanup_tags


@click.group("companies")
def cli():
    """Companies chapter."""


@cli.command("ratings")
@click.option(
    "-y", "--year",
    type=int,
    default=datetime.now().year - 1,
    show_default=True,
    help="",
)
@click.option(
    "-s", "--size",
    type=click.Choice(CompanySize),
    default=CompanySize.HUGE,
    show_default=True,
    help="""\b
    5: Over 5000
    4: 1000 - 5000
    3: 100 - 1000
    2: 10 - 100
    
    Размер компании.
    """,
)
@click.option(
    "-S", "--sort",
    type=click.Choice(CompanyRatingCriteria),
    default=CompanyRatingCriteria.AV,
    show_default=True,
    help="""\b
    av: Общая оценка
    s_2: Интересные задачи
    s_16: Современные технологии
    s_3: Адекватная зарплата
    s_4: Социальный пакет
    s_5: Комфортные условия труда
    s_6: Профессиональный рост
    s_7: Карьерный рост
    s_8: Отношения с коллегами
    s_9: Признание результатов труда
    s_10: Грамотность менеджмента
    s_11: Связь с топ-менеджментом
    s_12: Компания делает мир лучше
    
    Критерии оценки.
    """,
)
@click.option(
    "-q", "--search",
    help="Search query.",
)
@click.option(
    "-p", "--page",
    type=int,
    default=Pagination.INIT_PAGE,
    show_default=True,
    help="Page number.",
)
@click.option(
    "--full-scores/--no-full-scores",
    default=False,
    show_default=True,
    help="",
)
@click.option(
    "--json/--no-json", "as_json",
    default=False,
    show_default=True,
    help="Show as JSON.",
)
@click.pass_obj
@process_response_error
def get_companies_ratings(
        client: HABRCareerClient,
        year: int,
        size: CompanySize,
        sort: CompanyRatingCriteria,
        search: str,
        page: int,
        full_scores: bool,
        as_json: bool,
) -> None:
    """Get companies ratings."""
    console = Console()

    with console.status("Loading...", spinner=SPINNER):
        result = client.get_companies_ratings(
            year=year,
            size=size,
            sort=sort,
            search=search,
            page=page,
        )

    if as_json:
        console.print(output_as_json(ratings=result))
        return

    meta = result.meta
    ratings = result.list_
    table_width = 100

    titles = [f"Ratings ({meta.total_results})"]
    captions = [
        ", ".join([
            f"{k.title().replace("_", " ")}: {v}"
            for k, v in meta.model_dump(
                exclude={"total_results", "counter_description"}).items()
        ]),
        # meta.counter_description.capitalize(),
    ]

    def build_scores_table(
            rating, no: int, *, show_extra: bool = False) -> Table:
        no += 1
        items = rating.scores.items
        extra = [
            (
                f"[bright_black]{s.title}[/bright_black]",
                f"[bright_black]{s.value}[/bright_black]"
                + ("" if i < len(items) - 1 else "\n")
            ) for i, s in enumerate(items)
        ] if show_extra else []

        return build_table(
            rows=[
                (
                    rating.scores.featured.title,
                    rating.scores.featured.value
                ),
                *extra
            ],
            box_=box.SIMPLE,
            show_edge=False,
            title=f"[blue]#{no} {rating.company.title} ⭑ {rating.summary.value}[/blue]",
            title_justify="left",
        )

    show_table(
        console=console,
        title="\n".join([t for t in titles if t]),
        rows=[
            (
                build_scores_table(x, i, show_extra=full_scores),
                "\n".join([
                    f"[blue]{x.company.description}[/blue]",
                    "[bright_black]" + " • ".join(x for x in [
                        x.company.location and x.company.location.title,
                        x.company.vacancies and x.company.vacancies.title,
                    ] if x) + "[/bright_black]\n",
                    "\n\n".join(x for x in [
                        cleanup_tags(x.review.summary),
                        x.review.positives and f"[blue]Pros[/blue]\n{cleanup_tags(x.review.positives)}",
                        x.review.negatives and f"[blue]Cons[/blue]\n{cleanup_tags(x.review.negatives)}",
                    ] if x) + ("\n" if i < len(ratings) - 1 else ""),
                ]),
            ) for i, x in enumerate(ratings)
        ],
        caption="\n".join([c for c in captions if c]),
        width=table_width,
    )


@cli.command("subscribe")
@click.option(
    "-i", "--company-id",
    required=True,
    help="Company ID.",
)
@click.pass_obj
@process_response_error
def subscribe(client: HABRCareerClient, company_id: str) -> None:
    """Subscribe company."""
    console = Console()
    with console.status("Subscribing...", spinner=SPINNER):
        client.subscribe_company(company_id)


@cli.command("unsubscribe")
@click.option(
    "-i", "--company-id",
    required=True,
    help="Company ID.",
)
@click.pass_obj
@process_response_error
def unsubscribe(client: HABRCareerClient, company_id: str) -> None:
    """Unsubscribe company."""
    console = Console()
    with console.status("Unsubscribing...", spinner=SPINNER):
        client.unsubscribe_company(company_id)


@cli.command("favorite")
@click.option(
    "-i", "--company-id",
    required=True,
    help="Company ID.",
)
@click.pass_obj
@process_response_error
def favorite(client: HABRCareerClient, company_id: str) -> None:
    """Add company to favorites list."""
    console = Console()
    with console.status("Adding...", spinner=SPINNER):
        client.favorite_company(company_id)


@cli.command("unfavorite")
@click.option(
    "-i", "--company-id",
    required=True,
    help="Company ID.",
)
@click.pass_obj
@process_response_error
def unfavorite(client: HABRCareerClient, company_id: str) -> None:
    """Remove company from favorites list."""
    console = Console()
    with console.status("Removing...", spinner=SPINNER):
        client.unfavorite_company(company_id)
