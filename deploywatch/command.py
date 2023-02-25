from dotenv import load_dotenv

from itertools import zip_longest

from deploywatch.history import History
from deploywatch.repository import get_repository_history
from deploywatch.deployment import get_deployment_history
from deploywatch.presentation import write_histories


def generate_histories(name: str, code_only: bool, limit: int):
    load_dotenv()
    histories = []

    repository_histories = get_repository_history(name, limit)

    # CircleCI
    deployment_histories = []
    if not code_only:
        sha_list = [rh.merge_commit_sha for rh in repository_histories]
        deployment_histories = get_deployment_history(name, sha_list, limit)

    for rh, dh in zip_longest(repository_histories, deployment_histories):
        histories.append(History(
            rh.first_committed_at,
            rh.merged_at,
            dh.deployed_at if dh is not None else None,
        ))

    write_histories('output.csv', histories)
