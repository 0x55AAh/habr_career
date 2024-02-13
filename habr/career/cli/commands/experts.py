import click
from rich import box
from rich.console import Console
from rich.text import Text

from habr.career.cli.config import SPINNER
from habr.career.cli.utils import (
    process_response_error,
    output_as_json,
    show_table,
    build_table,
)
from habr.career.client import HABRCareerClient
from habr.career.client.experts import RequestID, ExpertsOrder
from habr.career.utils import (
    Pagination,
    Currency,
    QualificationID,
    CurrencySymbol,
)


@click.group("experts")
def cli():
    """Experts chapter."""


@cli.command("list")
@click.option(
    "-R", "--order",
    type=click.Choice(ExpertsOrder),
    default=ExpertsOrder.LAST_ACTIVE,
    show_default=True,
    help="""\b
    lastActive: По дате визита
    rate_desc: Цена по убыванию
    rate_asc: Цена по возрастанию
    
    Сортировка.
    """,
)
@click.option(
    "-O", "--free-only",
    is_flag=True,
    default=None,
    help="Бесплатно.",
)
@click.option(
    "-F", "--free-intro",
    is_flag=True,
    default=None,
    help="Первая встреча бесплатно.",
)
@click.option(
    "-S", "--skills",
    multiple=True,
    type=int,
    help="Какие навыки вы хотите развить.",
)
@click.option(
    "-Z", "--specializations",
    multiple=True,
    type=int,
    help="Специализация.",
)
@click.option(
    "-Q", "--qualification",
    type=click.Choice(QualificationID),
    help="""\b
    1: Intern
    3: Junior
    4: Middle
    5: Senior
    6: Lead
    
    Ваша квалификация.
    """,
)
@click.option(
    "-C", "--currency",
    type=click.Choice(Currency),
    default=Currency.RUR,
    show_default=True,
    help="Валюта.",
)
@click.option(
    "-f", "--rate-from",
    type=int,
    help="Стоимость часа от.",
)
@click.option(
    "-t", "--rate-to",
    type=int,
    help="Стоимость часа до.",
)
@click.option(
    "-r", "--request",
    type=click.Choice(RequestID),
    help="""\b
    1: Начало карьеры или смена профессии
    2: Развитие навыков
    3: Оценка
    4: Смена работы
    5: Карьерный рост
    6: Помощь с задачей
    7: Поддержка и коучинг
    8: Карьера за рубежом
    
    Ваш запрос.
    """,
)
@click.option(
    "-q", "--search",
    help="Поиск по навыкам, целям, имени.",
)
@click.option(
    "-p", "--page",
    type=int,
    default=Pagination.INIT_PAGE,
    show_default=True,
    help="Page number.",
)
@click.option(
    "-P", "--per-page",
    type=int,
    default=Pagination.PER_PAGE,
    show_default=True,
    help="Items per page.",
)
@click.option(
    "--json/--no-json", "as_json",
    default=False,
    show_default=True,
    help="Show as JSON.",
)
@click.pass_obj
@process_response_error
def get_experts(
    client: HABRCareerClient,
    order: str | None,
    free_only: bool | None,
    free_intro: bool | None,
    skills: list[int] | None,
    specializations: list[int] | None,
    qualification: QualificationID | None,
    currency: Currency | None,
    rate_from: int | None,
    rate_to: int | None,
    request: RequestID | None,
    search: str | None,
    page: int,
    per_page: int,
    as_json: bool,
):
    """Get experts list."""
    console = Console()

    kwargs = {
        "order": order,
        "free_only": free_only,
        "free_intro": free_intro,
        "skills": skills,
        "specializations": specializations,
        "qualification": qualification,
        "currency": currency,
        "rate_from": rate_from,
        "rate_to": rate_to,
        "request": request,
        "search": search,
        "page": page,
        "per_page": per_page,
    }

    with console.status("Loading...", spinner=SPINNER):
        result = client.get_experts(**kwargs)

    if as_json:
        console.print(output_as_json(experts=result))
        return

    meta = result.meta
    total_count = meta.total

    if not total_count:
        console.print(Text("No experts", style="blue"))
        return

    experts = result.objects

    table_width = 100

    rows = []
    for expert in experts:
        full_name = expert.title
        username = expert.login
        age = expert.age and expert.age.title
        experience = expert.experience.title

        last_job_company = expert.last_job and expert.last_job.company.title
        last_job_position = expert.last_job and expert.last_job.position
        last_job_duration = expert.last_job and expert.last_job.duration.title
        last_job_accredited = expert.last_job and expert.last_job.company.accredited
        last_job = [last_job_company, last_job_position, last_job_duration]

        qualifications = [x.title for x in expert.qualifications]
        specializations = [x.title for x in expert.specializations]
        skills = [x.title for x in expert.skills]

        rate_value = expert.rate and expert.rate.amount
        rate_currency = expert.rate and CurrencySymbol.by_name(expert.rate.currency)
        free_intro = expert.rate and expert.rate.free_intro

        last_visited = expert.last_visited.title

        score_connections = expert.score.connections
        score_average = expert.score.average_score
        score_count = expert.score.scores_count

        requests_table = build_table(
            rows=[
                expert.requests and (
                    Text(x.title, style="bright_black"),
                    " • ".join([i.title for i in x.items]),
                ) for x in expert.requests
            ],
            box_=box.SIMPLE,
            show_edge=False,
        )
        skills_table = build_table(
            rows=[
                x for x in [skills and (
                    Text("Skills", style="bright_black"),
                    " • ".join(skills)
                )] if x
            ],
            box_=box.SIMPLE,
            show_edge=False,
        )
        specializations_table = build_table(
            rows=[
                x for x in [specializations and (
                    Text("Specializations", style="bright_black"),
                    " • ".join(specializations)
                )] if x
            ],
            box_=box.SIMPLE,
            show_edge=False,
        )
        qualifications_table = build_table(
            rows=[
                x for x in [qualifications and (
                    Text("Qualifications", style="bright_black"),
                    " • ".join(qualifications)
                )] if x
            ],
            box_=box.SIMPLE,
            show_edge=False,
        )
        general_table = build_table(
            rows=[
                (Text("\n").join([
                    Text(" • ").join(Text(x) for x in [age, experience] if x),
                    Text(" • ").join(Text(x) for x in last_job if x),
                ]),),
            ],
            box_=box.SIMPLE,
            show_edge=False,
        )
        rate_table = build_table(
            rows=[
                (" • ".join(x for x in [
                    f"{rate_value} {rate_currency} / час",
                    "Первая встреча бесплатно" if free_intro else "",
                ] if x) if expert.rate else "Бесплатно",),
            ],
            box_=box.SIMPLE,
            show_edge=False,
        )
        scores_table = build_table(
            rows=[
                (
                    Text("Консультаций", style="bright_black"),
                    str(score_connections)
                ),
                (
                    Text("Средняя оценка", style="bright_black"),
                    str(score_average)
                ),
                (
                    Text("Оценок", style="bright_black"),
                    str(score_count)
                ),
            ],
            box_=box.SIMPLE,
            show_edge=False,
        )

        tables = [
            t for t in [
                    general_table,
                    scores_table,
                    qualifications_table,
                    specializations_table,
                    skills_table,
                    requests_table,
                    rate_table,
            ] if t.rows
        ]
        table_rows = []
        for table in tables:
            table_rows.append([table])
            table_rows.append([Text()])

        del table_rows[-1]

        summary_table = build_table(
            rows=table_rows,
            box_=box.SIMPLE,
            show_edge=False,
        )

        rows.append([
            Text("\n").join([
                Text(full_name, style="blue"),
                Text(username, style="bright_black"),
                Text(last_visited),
            ]),
            summary_table,
        ])

    show_table(
        console=console,
        title=f"Эксперты ({total_count})",
        rows=rows,
        caption=", ".join([
            f"{k.title().replace("_", " ")}: {v}"
            for k, v in meta.model_dump(exclude={"total"}).items()
        ]),
        width=table_width,
    )
