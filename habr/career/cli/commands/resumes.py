import click
from rich import box
from rich.console import Console
from rich.text import Text

from habr.career.cli.config import SPINNER, EXPERT_MARK
from habr.career.cli.utils import (
    process_response_error,
    output_as_json,
    show_table,
    build_table,
)
from habr.career.client import HABRCareerClient
from habr.career.client.resumes import (
    CareerSearchField,
    CareerActivityPeriod,
    CareerSortingCriteria,
    CareerWorkState,
)
from habr.career.utils import (
    Pagination,
    Currency,
    QualificationID,
)


@click.group("resumes")
def cli():
    """Resumes chapter."""


@cli.group("filters")
def filters():
    """Performs operations on resume filters."""


@cli.command("list")
@click.option(
    "-R", "--relocation",
    is_flag=True,
    default=None,
    help="Готов к переезду.",
)
@click.option(
    "-r", "--remote",
    is_flag=True,
    default=None,
    help="Готов к удалённой работе.",
)
@click.option(
    "-D", "--period",
    type=CareerActivityPeriod,
    help="""\b
    two_years:    За 2 года
    year:         За 1 год
    half_year:    За 6 месяцев
    three_months: За 3 месяца
    
    Активность на сайте.
    """,
)
@click.option(
    "-e", "--with-educations",
    is_flag=True,
    default=None,
    help="С высшим образованием.",
)
@click.option(
    "-E", "--with-extra-educations",
    is_flag=True,
    default=None,
    help="С дополнительным образованием.",
)
@click.option(
    "-X", "--with-experiences",
    is_flag=True,
    default=None,
    help="С опытом работы.",
)
@click.option(
    "-S", "--with-salary",
    is_flag=True,
    default=None,
    help="Указана зарплата.",
)
@click.option(
    "-T", "--with-social-ratings",
    is_flag=True,
    default=None,
    help="Участник ИТ-сообществ.",
)
@click.option(
    "-q", "--search",
    help="Search query.",
)
@click.option(
    "-F", "--search-fields",
    multiple=True,
    type=CareerSearchField,
    help="""\b
    fio:             в имени
    resume_headline: в специализации
    experiences:     в должностях
    skills:          в навыках профиля
    social_tags:     в навыках сообществ
    
    Поиск по полям.
    """,
)
@click.option(
    "-O", "--sort",
    type=CareerSortingCriteria,
    help="""\b
    last_visited: по дате визита
    relevance:    по соответствию
    salary_desc:  по убыванию зарплаты
    salary_asc:   по возрастанию зарплаты
    
    Сортировка.
    """,
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
    
    Квалификация.
    """,
)
@click.option(
    "-K", "--skills",
    multiple=True,
    type=int,
    help="Профессиональные навыки.",
)
@click.option(
    "-s", "--salary",
    type=int,
    help="Вознаграждение.",
)
@click.option(
    "-c", "--currency",
    type=click.Choice(Currency),
    default=Currency.RUR,
    show_default=True,
    help="Валюта вознаграждения.",
)
@click.option(
    "-L", "--locations",
    multiple=True,
    type=str,
    help="Местоположение.",
)
@click.option(
    "-l", "--exclude-locations",
    is_flag=True,
    default=None,
    help="Исключить местоположение.",
)
@click.option(
    "-C", "--companies",
    multiple=True,
    type=int,
    help="Компания.",
)
@click.option(
    "-M", "--not-companies",
    is_flag=True,
    default=None,
    help="Исключить компанию.",
)
@click.option(
    "-Y", "--current-company",
    is_flag=True,
    default=None,
    help="Текущее место работы.",
)
@click.option(
    "-V", "--universities",
    multiple=True,
    type=int,
    help="Высшее образование.",
)
@click.option(
    "-N", "--not-universities",
    is_flag=True,
    default=None,
    help="Исключить из поиска высшее образование.",
)
@click.option(
    "-I", "--educations",
    multiple=True,
    type=int,
    help="Доп образование.",
)
@click.option(
    "-U", "--not-educations",
    is_flag=True,
    default=None,
    help="Исключить из поиска доп образование.",
)
@click.option(
    "-W", "--work-state",
    type=CareerWorkState,
    help="""\b
    not_search: Не ищу работу
    search:     Ищу работу
    ready:      Рассмотрю предложения
    
    Готовность к работе.
    """,
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
def get_resumes(
    client: HABRCareerClient,
    relocation: bool | None,
    remote: bool | None,
    period: CareerActivityPeriod | None,

    with_educations: bool | None,
    with_extra_educations: bool | None,
    with_experiences: bool | None,
    with_salary: bool | None,
    with_social_ratings: bool | None,

    search: str | None,
    search_fields: list[CareerSearchField] | None,

    sort: CareerSortingCriteria | None,
    specializations: list[int] | None,
    qualification: QualificationID | None,
    skills: list[int] | None,
    salary: int | None,
    currency: Currency | None,
    locations: list[str] | None,
    exclude_locations: bool | None,
    companies: list[int] | None,
    not_companies: bool | None,
    current_company: bool | None,
    universities: list[int] | None,
    not_universities: bool | None,
    educations: list[int] | None,
    not_educations: bool | None,
    work_state: CareerWorkState | None,

    page: int,
    per_page: int,
    as_json: bool,
) -> None:
    """Get resumes list."""
    console = Console()

    kwargs = {
            "search": search,
            "search_fields": search_fields,

            "sort": sort,
            "specializations": specializations,
            "qualification": qualification,
            "skills": skills,
            "salary": salary,
            "currency": currency,
            "locations": locations,
            "exclude_locations": exclude_locations,
            "companies": companies,
            "not_companies": not_companies,
            "current_company": current_company,
            "universities": universities,
            "not_universities": not_universities,
            "educations": educations,
            "not_educations": not_educations,
            "work_state": work_state,

            "relocation": relocation,
            "remote": remote,
            "period": period,

            "with_educations": with_educations,
            "with_extra_educations": with_extra_educations,
            "with_experiences": with_experiences,
            "with_salary": with_salary,
            "with_social_ratings": with_social_ratings,

            "page": page,
            "per_page": per_page,
        }

    with console.status("Loading...", spinner=SPINNER):
        result = client.get_resumes(**kwargs)

    if as_json:
        console.print(output_as_json(resumes=result))
        return

    if not len(result.objects):
        console.print(Text("No resumes", style="blue"))
        return

    show_resumes_table(console, result)


def show_resumes_table(console, result):
    meta = result.meta
    total_count = meta.total_results

    table_width = 100

    rows = []
    for resume in result.objects:
        full_name = resume.title
        username = resume.id
        last_visited = resume.last_visited.title
        salary = resume.salary and resume.salary.title
        qualification = resume.qualification and resume.qualification.title
        availability = resume.availability.title
        specializations = [x.title for x in resume.specializations]
        age = resume.age and resume.age.title
        experience = resume.experience.title
        companies_count = resume.companies_count
        location = resume.location and resume.location.title
        relocation = resume.relocation and "Готов к переезду"
        remote_work = resume.remote_work and "Готов к удалённой работе"
        education_university = (
                resume.education and resume.education.university.title)
        education_duration = (
                resume.education and resume.education.duration.title)
        education_faculty = (
                resume.education and resume.education.faculty)
        more_university_count = (
                resume.more_university_count
                and f"Ещё {resume.more_university_count} в профиле")
        additional_education = [x.title for x in resume.additional_education]
        communities = [x.title for x in resume.communities]
        expert_mark = f" {EXPERT_MARK}" if resume.is_expert else ""

        general_table = build_table(
            rows=[
                (Text("\n\n").join([
                    Text(" • ").join([
                        Text(x) for x in [*specializations, qualification] if x
                    ]),
                    Text(" • ").join([
                        Text(x) for x in [salary, availability] if x
                    ]),
                    Text(" • ").join([Text(x.title) for x in resume.skills]),
                ]),)
            ],
            box_=box.SIMPLE,
            show_edge=False,
        )
        personal_table = build_table(
            rows=[(h, v) for h, v in [
                (
                    Text("Возраст", style="bright_black"),
                    age,
                ),
                (
                    Text("Опыт работы", style="bright_black"),
                    " • ".join(x for x in [companies_count, experience] if x)
                ),
                (
                    Text("Город", style="bright_black"),
                    " • ".join(x for x in [
                        location, remote_work, relocation] if x),
                ),
                (
                    Text("Высшее образование", style="bright_black"),
                    Text(" • ").join(x for x in [
                        education_university and Text(education_university),
                        education_faculty and Text(education_faculty),
                        Text("\n").join(x for x in [
                            education_duration and Text(education_duration),
                            (
                                    more_university_count
                                    and Text(
                                        more_university_count,
                                        style="bright_black"
                                    )
                            ),
                        ] if x),
                    ] if x),
                ),
                (
                    Text("Дополнительное образование",
                         style="bright_black"),
                    " • ".join(additional_education),
                ),
                (
                    Text("Участие в профессиональных сообществах",
                         style="bright_black"),
                    " • ".join(communities),
                ),
            ] if v],
            box_=box.SIMPLE,
            show_edge=False,
        )

        tables = [
            t for t in [general_table, personal_table]
            if t.rows
        ]

        table_rows = []
        for table in tables:
            table_rows.append([table])
            table_rows.append([Text()])

        summary_table = build_table(
            rows=table_rows,
            box_=box.SIMPLE,
            show_edge=False,
        )

        rows.append([
            Text("\n").join([
                Text(f"{full_name}{expert_mark}", style="blue"),
                Text(username, style="bright_black"),
                Text(last_visited),
            ]),
            summary_table,
        ])

    limited_access = result.limited_access and "Поиск ограничен"
    # TODO:
    #  type = noCompany
    #  type = guest

    show_table(
        console=console,
        title=f"Специалисты ({total_count})",
        rows=rows,
        caption="\n".join(x for x in [
            ", ".join([
                f"{k.title().replace("_", " ")}: {v}"
                for k, v in meta.model_dump(
                    exclude={"total_results"}).items()
            ]),
            limited_access and f"[red]{limited_access}[/red]",
        ] if x),
        width=table_width,
    )


@filters.command("save")
@click.option(
    "-R", "--relocation",
    is_flag=True,
    default=None,
    help="Готов к переезду.",
)
@click.option(
    "-r", "--remote",
    is_flag=True,
    default=None,
    help="Готов к удалённой работе.",
)
@click.option(
    "-D", "--period",
    type=CareerActivityPeriod,
    help="""\b
    two_years:    За 2 года
    year:         За 1 год
    half_year:    За 6 месяцев
    three_months: За 3 месяца

    Активность на сайте.
    """,
)
@click.option(
    "-e", "--with-educations",
    is_flag=True,
    default=None,
    help="С высшим образованием.",
)
@click.option(
    "-E", "--with-extra-educations",
    is_flag=True,
    default=None,
    help="С дополнительным образованием.",
)
@click.option(
    "-X", "--with-experiences",
    is_flag=True,
    default=None,
    help="С опытом работы.",
)
@click.option(
    "-S", "--with-salary",
    is_flag=True,
    default=None,
    help="Указана зарплата.",
)
@click.option(
    "-T", "--with-social-ratings",
    is_flag=True,
    default=None,
    help="Участник ИТ-сообществ.",
)
@click.option(
    "-q", "--search",
    help="Search query.",
)
@click.option(
    "-F", "--search-fields",
    multiple=True,
    type=CareerSearchField,
    help="""\b
    fio:             в имени
    resume_headline: в специализации
    experiences:     в должностях
    skills:          в навыках профиля
    social_tags:     в навыках сообществ

    Поиск по полям.
    """,
)
@click.option(
    "-O", "--sort",
    type=CareerSortingCriteria,
    help="""\b
    last_visited: по дате визита
    relevance:    по соответствию
    salary_desc:  по убыванию зарплаты
    salary_asc:   по возрастанию зарплаты

    Сортировка.
    """,
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

    Квалификация.
    """,
)
@click.option(
    "-K", "--skills",
    multiple=True,
    type=int,
    help="Профессиональные навыки.",
)
@click.option(
    "-s", "--salary",
    type=int,
    help="Вознаграждение.",
)
@click.option(
    "-c", "--currency",
    type=click.Choice(Currency),
    default=Currency.RUR,
    show_default=True,
    help="Валюта вознаграждения.",
)
@click.option(
    "-L", "--locations",
    multiple=True,
    type=str,
    help="Местоположение.",
)
@click.option(
    "-l", "--exclude-locations",
    is_flag=True,
    default=None,
    help="Исключить местоположение.",
)
@click.option(
    "-C", "--companies",
    multiple=True,
    type=int,
    help="Компания.",
)
@click.option(
    "-M", "--not-companies",
    is_flag=True,
    default=None,
    help="Исключить компанию.",
)
@click.option(
    "-Y", "--current-company",
    is_flag=True,
    default=None,
    help="Текущее место работы.",
)
@click.option(
    "-V", "--universities",
    multiple=True,
    type=int,
    help="Высшее образование.",
)
@click.option(
    "-N", "--not-universities",
    is_flag=True,
    default=None,
    help="Исключить из поиска высшее образование.",
)
@click.option(
    "-I", "--educations",
    multiple=True,
    type=int,
    help="Доп образование.",
)
@click.option(
    "-U", "--not-educations",
    is_flag=True,
    default=None,
    help="Исключить из поиска доп образование.",
)
@click.option(
    "-W", "--work-state",
    type=CareerWorkState,
    help="""\b
    not_search: Не ищу работу
    search:     Ищу работу
    ready:      Рассмотрю предложения

    Готовность к работе.
    """,
)
@click.pass_obj
@process_response_error
def save_careers_filter(
    client: HABRCareerClient,

    relocation: bool | None,
    remote: bool | None,
    period: CareerActivityPeriod | None,

    with_educations: bool | None,
    with_extra_educations: bool | None,
    with_experiences: bool | None,
    with_salary: bool | None,
    with_social_ratings: bool | None,

    search: str | None,
    search_fields: list[CareerSearchField] | None,

    sort: CareerSortingCriteria | None,
    specializations: list[int] | None,
    qualification: QualificationID | None,
    skills: list[int] | None,
    salary: int | None,
    currency: Currency | None,
    locations: list[str] | None,
    exclude_locations: bool | None,
    companies: list[int] | None,
    not_companies: bool | None,
    current_company: bool | None,
    universities: list[int] | None,
    not_universities: bool | None,
    educations: list[int] | None,
    not_educations: bool | None,
    work_state: CareerWorkState | None,
) -> None:
    """Save filter."""
    console = Console()

    kwargs = {
        "search": search,
        "search_fields": search_fields,

        "sort": sort,
        "specializations": specializations,
        "qualification": qualification,
        "skills": skills,
        "salary": salary,
        "currency": currency,
        "locations": locations,
        "exclude_locations": exclude_locations,
        "companies": companies,
        "not_companies": not_companies,
        "current_company": current_company,
        "universities": universities,
        "not_universities": not_universities,
        "educations": educations,
        "not_educations": not_educations,
        "work_state": work_state,

        "relocation": relocation,
        "remote": remote,
        "period": period,

        "with_educations": with_educations,
        "with_extra_educations": with_extra_educations,
        "with_experiences": with_experiences,
        "with_salary": with_salary,
        "with_social_ratings": with_social_ratings,
    }

    with console.status("Saving...", spinner=SPINNER):
        client.save_careers_filter(**kwargs)


@filters.command("delete")
@click.option(
    "-i", "--filter-id",
    type=int,
    help="Filter ID.",
)
@click.pass_obj
@process_response_error
def delete_careers_filter(
    client: HABRCareerClient,
    filter_id: int,
) -> None:
    """Delete filter."""
    console = Console()

    with console.status("Deleting...", spinner=SPINNER):
        client.delete_careers_filter(filter_id)


@filters.command("list")
@click.option(
    "--json/--no-json", "as_json",
    default=False,
    show_default=True,
    help="Show as JSON.",
)
@click.pass_obj
@process_response_error
def get_careers_filters(client: HABRCareerClient, as_json: bool) -> None:
    """List filters."""
    console = Console()

    with console.status("Loading...", spinner=SPINNER):
        result = client.get_resumes_data()
        filters_ = result["search"]["savedFilters"]

    if as_json:
        console.print(output_as_json(filters=filters_))
        return

    if not filters_:
        console.print(Text("No filters", style="blue"))
        return

    show_table(
        console=console,
        title=f"Сохраненные фильтры ({len(filters_)})",
        rows=[
            (Text(str(x["id"]), style="blue"), x["title"])
            for x in filters_
        ],
        width=100,
    )


@filters.command("apply")
@click.option(
    "-i", "--filter-id",
    type=int,
    help="Filter ID.",
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
def apply_career_filter(
    client: HABRCareerClient,
    filter_id: int,
    page: int,
    per_page: int,
    as_json: bool,
) -> None:
    """Apply filter."""
    console = Console()

    with console.status("Loading...", spinner=SPINNER):
        try:
            result = client.apply_career_filter(
                filter_id,
                page=page,
                per_page=per_page,
            )
        except KeyError:
            console.print(Text("Template not found", style="red"))
            exit(1)

    if as_json:
        console.print(output_as_json(resumes=result))
        return

    if not len(result.objects):
        console.print(Text("No resumes", style="blue"))
        return

    show_resumes_table(console, result)
