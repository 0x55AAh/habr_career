import click
from rich.console import Console

from habr.career.cli.config import SPINNER, DEFAULT_COLOR
from habr.career.cli.utils import (
    process_response_error,
    Choice,
    output_as_json,
)
from habr.career.cli.utils.chart import Chart
from habr.career.client import HABRCareerClient
from habr.career.client.salaries import EmploymentType
from habr.career.utils import ConcurrentJobs, Qualification, CurrencySymbol


@click.group("salaries")
def cli():
    """Salaries chapter."""


@cli.command("general_graph")
@click.option(
    "-q", "--qualification",
    type=click.Choice(Qualification),
    default=Qualification.ALL,
    show_default=True,
    help="",
)
@click.option(
    "-s", "--specializations",
    multiple=True,
    help="",
)
@click.option(
    "-r", "--remote",
    is_flag=True,
    default=None,
    help="",
)
@click.option(
    "-e", "--employment_type",
    type=Choice(EmploymentType),
    help="""\b
    0: Full time
    1: Part time
    """,
)
@click.option(
    "-c", "--company",
    help="",
)
@click.option(
    "-S", "--skills",
    multiple=True,
    help="",
)
@click.option(
    "-l", "--locations",
    multiple=True,
    help="",
)
@click.option(
    "-E", "--exclude_locations",
    is_flag=True,
    default=None,
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
def general_graph(
        client: HABRCareerClient,
        qualification: Qualification,
        specializations: list[str] | None,
        remote: bool | None,
        employment_type: EmploymentType | None,
        company: str | None,
        skills: list[str] | None,
        locations: list[str] | None,
        exclude_locations: bool | None,
        as_json: bool,
) -> None:
    """Show general salary graph."""
    console = Console()
    jobs = ConcurrentJobs()

    filter_ = {
        "specializations": specializations,
        "remote": remote,
        "employment_type": employment_type,
        "company": company,
        "skills": skills,
        "locations": locations,
        "exclude_locations": exclude_locations,
    }

    with console.status("Loading...", spinner=SPINNER):
        general_graph_, my_salary_ = (
            jobs
            .register(client.get_salary_general_graph, **filter_)
            .register(client.my_salary)
            .run()
        )

    groups = {g.name: g for g in general_graph_.groups}
    graphs_data = groups[qualification]

    if as_json:
        console.print(
            output_as_json(
                my_salary=my_salary_,
                graphs_data=graphs_data,
            )
        )
        return

    my_current_salary = getattr(my_salary_.current_period, "value", None)

    chart = Chart(
        data=[
            (graphs_data.min,),
            (graphs_data.p25,),
            (graphs_data.median,),
            (my_current_salary,),
            (graphs_data.p75,),
            (graphs_data.max,)
        ],
        labels=[
            "10% зарабатывают меньше",
            "25% зарабатывают меньше",
            "50% зарабатывают меньше",
            "Моя зарплата",
            "75% зарабатывают меньше",
            "90% зарабатывают меньше",
        ],
        categories=[
            "Встречаются часто",
            "Встречаются редко",
        ],
        label_styles=(
            "bright_black",  # Встречаются редко
            DEFAULT_COLOR,   # Встречаются часто
            DEFAULT_COLOR,   # Встречаются часто
            "yellow",        # Моя зарплата
            DEFAULT_COLOR,   # Встречаются часто
            "bright_black",  # Встречаются редко
        ),
        category_styles=(DEFAULT_COLOR, "bright_black"),
        title="\n".join([
            graphs_data.title,
            f"{graphs_data.salary.total} {CurrencySymbol.RUR}"
            f" = {graphs_data.salary.value} {CurrencySymbol.RUR} (зарплата)"
            f" + {graphs_data.salary.bonus} {CurrencySymbol.RUR} (премия)",
        ]),
        captions=[
            f"Рассчитано на основании {graphs_data.total} анкет",
            "Обновите свою зарплату" if not my_current_salary else "",
        ],
    )
    console.print(chart)


@cli.command("dynamic_graph")
@click.option(
    "-q", "--qualification",
    type=click.Choice(Qualification),
    default=Qualification.ALL,
    show_default=True,
    help="",
)
@click.option(
    "-s", "--specializations",
    multiple=True,
    help="",
)
@click.option(
    "-r", "--remote",
    is_flag=True,
    default=None,
    help="",
)
@click.option(
    "-e", "--employment_type",
    type=Choice(EmploymentType),
    help="""\b
    0: Full time
    1: Part time
    """,
)
@click.option(
    "-c", "--company",
    help="",
)
@click.option(
    "-S", "--skills",
    multiple=True,
    help="",
)
@click.option(
    "-l", "--locations",
    multiple=True,
    help="",
)
@click.option(
    "-E", "--exclude_locations",
    is_flag=True,
    default=None,
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
def dynamic_graph(
        client: HABRCareerClient,
        qualification: Qualification,
        specializations: list[str] | None,
        remote: bool | None,
        employment_type: EmploymentType | None,
        company: str | None,
        skills: list[str] | None,
        locations: list[str] | None,
        exclude_locations: bool | None,
        as_json: bool,
) -> None:
    """Show dynamic salary graph."""
    console = Console()
    jobs = ConcurrentJobs()

    filter_ = {
        "qualification": qualification,
        "specializations": specializations,
        "remote": remote,
        "employment_type": employment_type,
        "company": company,
        "skills": skills,
        "locations": locations,
        "exclude_locations": exclude_locations,
    }

    with console.status("Loading...", spinner=SPINNER):
        dynamic_graph_, my_salary_ = (
            jobs
            .register(client.get_salary_dynamic_graph, **filter_)
            .register(client.my_salary)
            .run()
        )

    if as_json:
        return console.print(
            output_as_json(
                my_salary=my_salary_,
                graphs_data=dynamic_graph_.graphs_data,
            )
        )

    chart = Chart(
        data=map(
            lambda x: x if x[1] else x[:1],
            zip(
                [p.value for p in dynamic_graph_.graphs_data.periods],
                [p.value for p in my_salary_.periods],
            )
        ),
        labels=[
            p.title
            for p in dynamic_graph_.graphs_data.periods
        ],
        categories=[
            dynamic_graph_.graphs_data.title,
            "Моя зарплата",
        ],
        category_styles=(DEFAULT_COLOR, "yellow"),
        title="Зарплаты в динамике",
    )
    console.print(chart)
