from datetime import datetime

import click
from rich import box
from rich.console import Console
from rich.table import Table

from habr.career.cli.config import SPINNER
from habr.career.cli.utils import (
    process_response_error,
    Choice,
    show_table,
    build_table,
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
    type=Choice(CompanySize),
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
    help="",
)
@click.option(
    "-p", "--page",
    type=int,
    default=Pagination.INIT_PAGE,
    show_default=True,
    help="",
)
@click.option(
    "--full-scores/--no-full-scores",
    default=False,
    show_default=True,
    help="",
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
