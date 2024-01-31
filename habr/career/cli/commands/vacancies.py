import click
from rich.console import Console
from rich.text import Text

from habr.career.cli.config import SPINNER
from habr.career.cli.utils import (
    process_response_error,
    Choice,
    output_as_json,
    show_table,
)
from habr.career.client import HABRCareerClient
from habr.career.client.vacancies import (
    EmploymentType,
    VacancyType,
    VacanciesSort,
)
from habr.career.utils import (
    Pagination,
    QualificationID,
    Currency, cleanup_tags,
)


@click.group("vacancies")
def cli():
    """Vacancies chapter."""


@cli.group("responses")
def responses():
    """Operations on responses."""


@cli.group("favorites")
def favorites():
    """Operations on favorites."""


@cli.group("reactions")
def reactions_():
    """Operations on reactions."""


@cli.command("list")
@click.option(
    "-R", "--sort",
    type=click.Choice(VacanciesSort),
    default=VacanciesSort.RELEVANCE,
    show_default=True,
    help="",
)
@click.option(
    "-t", "--type", "type_",
    type=click.Choice(VacancyType),
    default=VacancyType.ALL,
    show_default=True,
    help="",
)
@click.option(
    "-E", "--employment-type",
    type=click.Choice(EmploymentType),
    help="",
)
@click.option(
    "-C", "--currency",
    type=click.Choice(Currency),
    default=Currency.RUR,
    show_default=True,
    help="",
)
@click.option(
    "-Z", "--specializations",
    multiple=True,
    type=int,
    help="",
)
@click.option(
    "-L", "--locations",
    multiple=True,
    help="",
)
@click.option(
    "-e", "--exclude-company",
    is_flag=True,
    default=None,
    help="",
)
@click.option(
    "-H", "--has-accreditation",
    is_flag=True,
    default=None,
    help="",
)
@click.option(
    "-w", "--with-salary",
    is_flag=True,
    default=None,
    help="",
)
@click.option(
    "-s", "--salary",
    type=int,
    help="",
)
@click.option(
    "-Q", "--qualification",
    type=Choice(QualificationID),
    help="""\b
    1: Intern
    3: Junior
    4: Middle
    5: Senior
    6: Lead
    """,
)
@click.option(
    "-S", "--skills",
    multiple=True,
    type=int,
    help="",
)
@click.option(
    "-c", "--company",
    type=int,
    help="",
)
@click.option(
    "-r", "--remote",
    is_flag=True,
    default=None,
    help="",
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
    "-P", "--per-page",
    type=int,
    default=Pagination.PER_PAGE,
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
def get_vacancies(
    client: HABRCareerClient,
    sort: VacanciesSort | None,
    type_: VacancyType | None,
    employment_type: EmploymentType | None,
    currency: Currency | None,
    specializations: list[int] | None,
    locations: list[str] | None,
    exclude_company: bool | None,
    has_accreditation: bool | None,
    with_salary: bool | None,
    salary: int | None,
    qualification: QualificationID | None,
    skills: list[int] | None,
    company: int | None,
    remote: bool | None,
    search: str | None,
    page: int,
    per_page: int,
    as_json: bool,
) -> None:
    """Get vacancies."""
    console = Console()

    kwargs = {
        "sort": sort,
        "type_": type_,
        "employment_type": employment_type,
        "currency": currency,
        "specializations": specializations,
        "locations": locations,
        "exclude_company": exclude_company,
        "has_accreditation": has_accreditation,
        "with_salary": with_salary,
        "salary": salary,
        "qualification": qualification,
        "skills": skills,
        "company": company,
        "remote": remote,
        "search": search,
        "page": page,
        "per_page": per_page,
    }

    with console.status("Loading...", spinner=SPINNER):
        result = client.get_vacancies(**kwargs)

    if as_json:
        console.print(output_as_json(vacancies=result))
        return

    meta = result["meta"]
    total_count = meta["totalResults"]

    if not total_count:
        console.print("[blue]No vacancies[/blue]")
        return

    del meta["totalResults"]

    vacancies = result["list"]

    employment_descriptions = {
        "full_time": "Полный рабочий день",
        "part_time": "Неполный рабочий день",
        None: "",
    }

    table_width = 100

    rows = []
    for vacancy in vacancies:
        employment = employment_descriptions[vacancy["employment"]]
        remote = "Можно удаленно" if vacancy["remoteWork"] else ""
        salary = vacancy["salary"]["formatted"]
        qualification = vacancy["salaryQualification"]

        company = vacancy["company"]
        company_rating = company["rating"] or {}

        is_company_accredited = company["accredited"]
        company_rating_value = company_rating.get("value")
        company_rating_title = company_rating.get("title")

        favorite = vacancy["favorite"]
        archived = vacancy["archived"]
        hidden = vacancy["hidden"]

        rows.append([
            Text("\n").join([
                Text(str(vacancy["id"])),
                Text(
                    company["title"]
                    + (f" ⭑ {company_rating_value}" if company_rating_value else "")
                ),
                Text(vacancy["publishedDate"]["title"], style="bright_black"),
            ]),
            Text("\n").join(x for x in [
                Text(vacancy["title"], style="blue"),
                Text(" • ", style="bright_black").join(x for x in [
                    Text(", ", style="bright_black").join(
                        Text(location["title"], style="bright_black")
                        for location in vacancy["locations"] or []
                    ),
                    employment and Text(employment, style="bright_black"),
                    remote and Text(remote, style="bright_black"),
                ] if x),
                Text(salary and f"{salary}\n", style="bright_black"),
                Text(" • ").join([
                    Text(", ").join(x for x in [
                        Text("|").join(
                            Text(d["title"]) for d in vacancy["divisions"]
                        ),
                        qualification and Text(qualification["title"])
                    ] if x),
                    *[Text(skill["title"]) for skill in vacancy["skills"]],
                ]),
                Text(),
            ]),
        ])

    show_table(
        console=console,
        title=f"Работа и вакансии ({total_count})",
        rows=rows,
        caption=", ".join([f"{k}: {v}" for k, v in meta.items()]),
        width=table_width,
    )


@cli.command("get")
@click.option(
    "-i", "--id", "id_",
    type=int,
    required=True,
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
def get_vacancy(
    client: HABRCareerClient,
    id_: int,
    as_json: bool,
) -> None:
    """Get vacancy details."""
    console = Console()

    with console.status("Loading...", spinner=SPINNER):
        result = client.get_vacancy(id_=id_)

    vacancy = result["vacancy"]

    if as_json:
        console.print(output_as_json(vacancy=vacancy))
        return

    table_width = 100

    title = vacancy["title"]
    published_date = vacancy["publishedDate"]["title"]
    remote = vacancy["remoteWork"]
    is_marked = vacancy["isMarked"]
    favorite = vacancy["favorite"]
    archived = vacancy["archived"]
    hidden = vacancy["hidden"]
    description = vacancy["description"]
    cities = vacancy["humanCityNames"]
    short_geo = vacancy["shortGeo"]
    employment_type = vacancy["employmentType"]
    qualification = vacancy["salaryQualification"]
    skills = [x["title"] for x in vacancy["skills"]]
    divisions = [x["title"] for x in vacancy["divisions"]]
    salary = vacancy["salary"]
    bonuses = vacancy["bonuses"]
    instructions = vacancy["instructions"]
    team = vacancy["team"]
    candidate = vacancy["candidate"]

    def show_vacancy_meta_table():
        rows = [
            ("Зарплата", Text(salary["formatted"], end="\n\n")),
            (
                "Требования",
                Text(" • ").join([
                    Text(", ").join([
                        Text("|".join(divisions)),
                        Text(qualification["title"]),
                    ]),
                    Text(" • ".join(skills) + "\n"),
                ])
            ),
            (
                "Местоположение и тип занятости",
                " • ".join(x for x in [
                    cities,
                    employment_type,
                    "Можно удаленно" if remote else "",
                ] if x)),
        ]

        titles = [f"{title} ({published_date})"]

        show_table(
            console=console,
            title="\n".join(t for t in titles if t),
            rows=[
                (Text(h, style="blue"), x1)
                for h, x1 in rows if x1
            ],
            width=table_width,
            show_lines=False,
        )

    def show_about_vacancy_table():
        rows = [
            ("О компании и команде", cleanup_tags(team)),
            ("Ожидания от кандидата", cleanup_tags(candidate)),
            ("Условия работы", cleanup_tags(description)),
            ("Бонусы", cleanup_tags(bonuses)),
            ("Дополнительные инструкции", cleanup_tags(instructions)),
        ]
        rows = [(h, x1) for h, x1 in rows if x1]

        titles = ["Описание вакансии"]

        show_table(
            console=console,
            title="\n".join(t for t in titles if t),
            rows=[
                (
                    Text(h, style="blue"),
                    Text(x1, end=("\n\n" if i < len(rows) - 1 else "\n"))
                ) for i, (h, x1) in enumerate(rows)
            ],
            width=table_width,
        )

    show_vacancy_meta_table()
    show_about_vacancy_table()


@favorites.command("add")
@click.option(
    "-i", "--id", "id_",
    type=int,
    required=True,
    help="Vacancy ID.",
)
@click.pass_obj
@process_response_error
def add_vacancy_to_favorites(
    client: HABRCareerClient,
    id_: int,
) -> None:
    """Add vacancy to favorites list."""
    console = Console()
    with console.status("Adding...", spinner=SPINNER):
        client.add_vacancy_to_favorites(id_=id_)


@favorites.command("remove")
@click.option(
    "-i", "--id", "id_",
    type=int,
    required=True,
    help="Vacancy ID.",
)
@click.pass_obj
@process_response_error
def remove_vacancy_from_favorites(
    client: HABRCareerClient,
    id_: int,
) -> None:
    """Remove vacancy from favorites list."""
    console = Console()
    with console.status("Removing...", spinner=SPINNER):
        client.remove_vacancy_from_favorites(id_=id_)


@reactions_.command("give")
@click.option(
    "-i", "--id", "id_",
    type=int,
    required=True,
    help="Vacancy ID.",
)
@click.option(
    "-r", "--reactions",
    multiple=True,
    required=True,
    help="Reactions aliases.",
)
@click.pass_obj
@process_response_error
def give_reactions_to_vacancy(
    client: HABRCareerClient,
    id_: int,
    reactions: list[str],
) -> None:
    """Give reactions to vacancy."""
    console = Console()
    with console.status("Giving...", spinner=SPINNER):
        client.give_reactions_to_vacancy(id_=id_, reactions=reactions)


@reactions_.command("remove")
@click.option(
    "-i", "--id", "id_",
    type=int,
    required=True,
    help="Vacancy ID.",
)
@click.pass_obj
@process_response_error
def give_reactions_to_vacancy(
    client: HABRCareerClient,
    id_: int,
) -> None:
    """Remove all reactions to vacancy."""
    console = Console()
    with console.status("Removing...", spinner=SPINNER):
        client.give_reactions_to_vacancy(id_=id_, reactions=[])


@responses.command("create")
@click.option(
    "-i", "--id", "id_",
    type=int,
    required=True,
    help="Vacancy ID.",
)
@click.pass_obj
@process_response_error
def respond_to_vacancy(
    client: HABRCareerClient,
    id_: int,
) -> None:
    """Respond to vacancy."""
    console = Console()
    with console.status("Creating...", spinner=SPINNER):
        client.respond_to_vacancy(id_=id_)


@responses.command("revoke")
@click.option(
    "-v", "--vacancy-id",
    type=int,
    required=True,
    help="Vacancy ID.",
)
@click.option(
    "-r", "--response-id",
    type=int,
    required=True,
    help="Response ID.",
)
@click.pass_obj
@process_response_error
def revoke_response_to_vacancy(
    client: HABRCareerClient,
    vacancy_id: int,
    response_id: int,
) -> None:
    """Revoke existing response to vacancy."""
    console = Console()
    with console.status("Revoking...", spinner=SPINNER):
        client.revoke_response_to_vacancy(
            vacancy_id=vacancy_id,
            response_id=response_id,
        )


@responses.command("update")
@click.option(
    "-v", "--vacancy-id",
    type=int,
    required=True,
    help="Vacancy ID.",
)
@click.option(
    "-r", "--response-id",
    type=int,
    required=True,
    help="Response ID.",
)
@click.option(
    "-b", "--body",
    required=True,
    help="Text message.",
)
@click.pass_obj
@process_response_error
def update_response_to_vacancy(
    client: HABRCareerClient,
    vacancy_id: int,
    response_id: int,
    body: str,
) -> None:
    """Update existing response to vacancy."""
    console = Console()
    with console.status("Updating...", spinner=SPINNER):
        client.update_response_to_vacancy(
            vacancy_id=vacancy_id,
            response_id=response_id,
            body=body,
        )


@responses.command("list")
@click.option(
    "-i", "--id", "id_",
    type=int,
    required=True,
    help="Vacancy ID.",
)
@click.option(
    "--json/--no-json", "as_json",
    default=False,
    show_default=True,
    help="",
)
@click.pass_obj
@process_response_error
def get_vacancy_responses(
    client: HABRCareerClient,
    id_: int,
    as_json: bool,
) -> None:
    """Get responses to vacancy."""
    console = Console()
    with console.status("Loading...", spinner=SPINNER):
        result = client.get_vacancy_responses(id_=id_)

    if as_json:
        console.print(output_as_json(responses=result))
        return

    responses_list = result["list"]
    meta = result["meta"]

    total_results = meta["totalResults"]

    if not total_results:
        console.print(Text("No responses."), style="red")
        return

    table_width = 100
    del meta["totalResults"]

    rows = [
        (
            Text("\n").join([
                Text(str(x["id"])),
                Text(x["publishedAt"], style="bright_black")
            ]),
            x["message"] or "[No message]"
        ) for x in responses_list
    ]

    show_table(
        console=console,
        title=f"Responses ({total_results})",
        rows=rows,
        width=table_width,
        caption=", ".join([f"{k}: {v}" for k, v in meta.items()]),
    )


@responses.command("list_favorite")
@click.option(
    "-i", "--id", "id_",
    type=int,
    required=True,
    help="Vacancy ID.",
)
@click.option(
    "--json/--no-json", "as_json",
    default=False,
    show_default=True,
    help="",
)
@click.pass_obj
@process_response_error
def get_vacancy_favorite_responses(
        client: HABRCareerClient,
        id_: int,
        as_json: bool,
) -> None:
    """Get responses to vacancy that was marked as favorite."""
    console = Console()
    with console.status("Loading...", spinner=SPINNER):
        result = client.get_vacancy_favorite_responses(id_=id_)

    if as_json:
        console.print(output_as_json(responses=result))
        return

    responses_list = result["list"]
    meta = result["meta"]

    total_results = meta["totalResults"]

    if not total_results:
        console.print(Text("No responses."), style="red")
        return

    table_width = 100

    rows = [
        (
            Text("\n").join([
                Text(str(x["id"])),
                Text(x["publishedAt"], style="bright_black")
            ]),
            x["message"] or "[No message]"
        ) for x in responses_list
    ]

    show_table(
        console=console,
        title=f"Responses ({total_results})",
        rows=rows,
        width=table_width,
    )


@responses.command("list_archived")
@click.option(
    "-i", "--id", "id_",
    type=int,
    required=True,
    help="Vacancy ID.",
)
@click.option(
    "--json/--no-json", "as_json",
    default=False,
    show_default=True,
    help="",
)
@click.pass_obj
@process_response_error
def get_vacancy_archived_responses(
        client: HABRCareerClient,
        id_: int,
        as_json: bool,
) -> None:
    """Get responses to vacancy that was moved to archive."""
    console = Console()
    with console.status("Loading...", spinner=SPINNER):
        result = client.get_vacancy_archived_responses(id_=id_)

    if as_json:
        console.print(output_as_json(responses=result))
        return

    responses_list = result["list"]
    meta = result["meta"]

    total_results = meta["totalResults"]

    if not total_results:
        console.print(Text("No responses."), style="red")
        return

    table_width = 100

    rows = [
        (
            Text("\n").join([
                Text(str(x["id"])),
                Text(x["publishedAt"], style="bright_black")
            ]),
            x["message"] or "[No message]"
        ) for x in responses_list
    ]

    show_table(
        console=console,
        title=f"Responses ({total_results})",
        rows=rows,
        width=table_width,
    )
