from github import Github
import os
from datetime import datetime, timezone

from deploywatch.history import RepositoryHistory


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
