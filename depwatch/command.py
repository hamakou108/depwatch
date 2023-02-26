from dotenv import load_dotenv

from depwatch.history import create_histories
from depwatch.repository import get_main_branch, get_repository_history
from depwatch.deployment import get_deployment_history
from depwatch.presentation import write_histories


def generate_histories(name: str, code_only: bool, limit: int):
    load_dotenv()

    base = get_main_branch(name)

    repository_histories = get_repository_history(name, base, limit)

    # CircleCI
    deployment_histories = []
    if not code_only:
        deployment_histories = get_deployment_history(name, base, limit)

    write_histories(
        "output.csv", create_histories(repository_histories, deployment_histories)
    )
