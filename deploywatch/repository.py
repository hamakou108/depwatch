from github import Github
import os
from datetime import datetime, timezone


class RepositoryHistory:
    def __init__(
            self,
            first_committed_at: datetime,
            merged_at: datetime,
            merge_commit_sha: str
    ):
        self.first_committed_at = first_committed_at
        self.merged_at = merged_at
        self.merge_commit_sha = merge_commit_sha


def get_repository_history(name: str) -> list[RepositoryHistory]:
    histories = []

    gh = Github(os.environ.get('GITHUB_ACCESS_TOKEN'))
    repo = gh.get_repo(name)
    pulls = repo.get_pulls(state='closed')

    for pr in pulls:
        first_committed_at: datetime = pr.get_commits()[0].commit.author.date.replace(tzinfo=timezone.utc)
        merged_at: datetime = pr.merged_at.replace(tzinfo=timezone.utc)
        merge_commit_sha: str = pr.merge_commit_sha

        histories.append(RepositoryHistory(
            first_committed_at,
            merged_at,
            merge_commit_sha
        ))

    return histories
