from github import Github
import os
from datetime import datetime, timezone


class RepositoryHistory:
    def __init__(
            self,
            first_committed_at: datetime,
            merged_at: datetime,
    ):
        self.first_committed_at = first_committed_at
        self.merged_at = merged_at


def get_repository_history(name: str):
    histories = []

    gh = Github(os.environ.get('GITHUB_ACCESS_TOKEN'))
    repo = gh.get_repo(name)
    pulls = repo.get_pulls(state='closed')

    for pr in pulls:
        first_committed_at: datetime = pr.get_commits()[0].commit.author.date.replace(tzinfo=timezone.utc)
        merged_at: datetime = pr.merged_at.replace(tzinfo=timezone.utc)

        histories.append(RepositoryHistory(
            first_committed_at,
            merged_at,
        ))

    return histories
