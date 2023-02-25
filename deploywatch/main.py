import typer
from rich import print

from deploywatch.command import generate_histories


def main(
        name: str,
        code_only: bool = typer.Option(False, help="do not retrieve deployment histories from CI"),
        limit: int = typer.Option(100, help="count limit for retrieving history"),
):
    generate_histories(name, code_only, limit)
    print(':sparkles::sparkles: [green]Completed![/green] :sparkles::sparkles:')


if __name__ == "__main__":
    typer.run(main)
