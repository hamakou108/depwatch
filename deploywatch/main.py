import typer
from rich import print

from deploywatch.command import History, generate_histories


def main(
        name: str,
        code_only: bool = typer.Option(False, help="do not retrieve deployment histories from CI")
):
    histories = generate_histories(name, code_only)
    print(",".join(History.keys()))
    for h in histories:
        print(",".join([v.isoformat() for v in h.values()]))


if __name__ == "__main__":
    typer.run(main)
