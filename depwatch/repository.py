from github import Github
import os
from datetime import datetime, timezone
from depwatch.exception import DepwatchException
from depwatch.history import RepositoryHistory


def get_main_branch(name: str) -> str:
    gh = Github(os.environ.get("GITHUB_ACCESS_TOKEN"))

    repo = gh.get_repo(name)
    branches = repo.get_branches()

    if "main" in [b.name for b in branches]:
        return "main"
    elif "master" in [b.name for b in branches]:
        return "master"
    else:
        raise DepwatchException("'main' or 'master' branch was not found")


def get_repository_history(name: str, base: str, limit: int) -> list[RepositoryHistory]:
    histories = []

    gh = Github(os.environ.get("GITHUB_ACCESS_TOKEN"), per_page=100)
    repo = gh.get_repo(name)
    pulls = repo.get_pulls(state="closed", base=base)[:limit]

    for p in pulls:
        if p.merged_at is None:
            continue

        first_committed_at: datetime = p.get_commits()[0].commit.author.date.replace(
            tzinfo=timezone.utc
        )
        merged_at: datetime = p.merged_at.replace(tzinfo=timezone.utc)
        merge_commit_sha: str = p.merge_commit_sha

        merge_commit = repo.get_commit(merge_commit_sha)
        check_runs = merge_commit.get_check_runs()
        check_run = check_runs[0] if check_runs.totalCount > 0 else None
        check_run_app_slug = check_run.app.slug if check_run is not None else None
        check_run_external_id = check_run.external_id if check_run is not None else None

        histories.append(
            RepositoryHistory(
                first_committed_at,
                merged_at,
                merge_commit_sha,
                check_run_app_slug,
                check_run_external_id,
            )
        )

    return histories
