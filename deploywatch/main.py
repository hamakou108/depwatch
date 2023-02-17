import typer
from deploywatch.command import Scope

def main(
    name: str,
    scope: Scope = Scope.all
):
    typer.echo(f"Hello {name}, {scope.value}!")

if __name__ == "__main__":
    typer.run(main)