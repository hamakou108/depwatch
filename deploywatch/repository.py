from github import Github
import os
from datetime import datetime, timezone

from deploywatch.history import RepositoryHistory


def get_repository_history(name: str, limit: int) -> list[RepositoryHistory]:
    histories = []

    gh = Github(os.environ.get('GITHUB_ACCESS_TOKEN'), per_page=100)
    repo = gh.get_repo(name)
    pulls = repo.get_pulls(state='closed')[:limit]

    for p in pulls:
        first_committed_at: datetime = p.get_commits()[0].commit.author.date.replace(tzinfo=timezone.utc)
        merged_at: datetime = p.merged_at.replace(tzinfo=timezone.utc)
        merge_commit_sha: str = p.merge_commit_sha

        histories.append(RepositoryHistory(
            first_committed_at,
            merged_at,
            merge_commit_sha
        ))

    return histories
