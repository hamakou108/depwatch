import typer
from rich import print

from depwatch.command import generate_histories


app = typer.Typer()


@app.command()
def main(
    name: str,
    code_only: bool = typer.Option(
        False, help="do not retrieve deployment histories from CI"
    ),
    limit: int = typer.Option(100, help="count limit for retrieving history"),
    workflow_name: str = typer.Option(
        None,
        help="The workflow name of the CI to be obtained. This is useful when there are multiple workflows triggered by commits to the main branch.",
    ),
):
    generate_histories(name, code_only, limit, workflow_name)
    print(":sparkles::sparkles: [green]Completed![/green] :sparkles::sparkles:")


def main_cli():
    app()


if __name__ == "__main__":
    app()
