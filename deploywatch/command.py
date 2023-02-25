from dotenv import load_dotenv
from datetime import datetime

from deploywatch.repository import get_repository_history
from deploywatch.deployment import get_deployment_history


class History:
    def __init__(
            self,
            first_committed_at: datetime,
            merged_at: datetime,
            deployed_at: datetime,
    ):
        self.first_committed_at = first_committed_at
        self.merged_at = merged_at
        self.deployed_at = deployed_at

    @staticmethod
    def keys() -> list[str]:
        return [
            'first_committed_at',
            'merged_at',
            'deployed_at',
        ]

    def values(self) -> list[datetime]:
        return [
            self.first_committed_at,
            self.merged_at,
            self.deployed_at
        ]

    def __eq__(self, other: 'History'):
        return (self.first_committed_at == other.first_committed_at
                and self.merged_at == other.merged_at
                and self.deployed_at == other.deployed_at)


def generate_histories(name: str, code_only: bool):
    load_dotenv()
    histories = []

    repository_histories = get_repository_history(name)

    # CircleCI
    deployment_histories = []
    if not code_only:
        sha_list = [rh.merge_commit_sha for rh in repository_histories]
        deployment_histories = get_deployment_history(name, sha_list)

    for rh, dh in zip(repository_histories, deployment_histories):
        histories.append(History(
            rh.first_committed_at,
            rh.merged_at,
            dh.deployed_at,
        ))

    return histories
