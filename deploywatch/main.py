import typer
from rich import print

from deploywatch.command import Scope, History, generate_histories


def main(
        name: str,
        scope: Scope = Scope.all
):
    histories = generate_histories(name, scope)
    print(",".join(History.keys()))
    for h in histories:
        print(",".join([v.isoformat() for v in h.values()]))


if __name__ == "__main__":
    typer.run(main)
