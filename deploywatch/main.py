import typer
from deploywatch.command import Scope
from rich import print

from command import History, generate_histories


def main(
        name: str,
        scope: Scope = Scope.all
):
    histories = generate_histories()
    print(",".join(History.keys()))
    for h in histories:
        print(",".join([v.isoformat() for v in h.values()]))


if __name__ == "__main__":
    typer.run(main)
