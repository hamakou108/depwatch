from datetime import datetime
import json
from typing import Optional

from depwatch.exception import DepwatchException


class History:
    def __init__(
        self,
        first_committed_at: datetime,
        merged_at: datetime,
        deployed_at: Optional[datetime],
    ):
        self.first_committed_at = first_committed_at
        self.merged_at = merged_at
        self.deployed_at = deployed_at

    @staticmethod
    def keys() -> list[str]:
        return [
            "first_committed_at",
            "merged_at",
            "deployed_at",
        ]

    def values(self) -> list:
        return [self.first_committed_at, self.merged_at, self.deployed_at]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, History):
            return NotImplemented
        return (
            self.first_committed_at == other.first_committed_at
            and self.merged_at == other.merged_at
            and self.deployed_at == other.deployed_at
        )


class RepositoryHistory:
    def __init__(
        self,
        first_committed_at: datetime,
        merged_at: datetime,
        merge_commit_sha: str,
        check_run_app_slug: str | None = None,
        check_run_external_id: str | None = None,
    ):
        self.first_committed_at = first_committed_at
        self.merged_at = merged_at
        self.merge_commit_sha = merge_commit_sha
        self.check_run_app_slug = check_run_app_slug
        self.check_run_external_id = check_run_external_id

    def get_workflow_id(self) -> str | None:
        if (
            self.check_run_app_slug is None
            or self.check_run_app_slug != "circleci-checks"
        ):
            return None

        if self.check_run_external_id is None:
            raise DepwatchException("'check_run.external_id' was not found")

        decoded_external_id = json.loads(self.check_run_external_id)

        return decoded_external_id.get("workflow-id")


def convert_repository_history_to_workflow_ids(
    repository_histories: list[RepositoryHistory],
) -> list[str]:
    raw_workflow_ids = [history.get_workflow_id() for history in repository_histories]
    return [x for x in raw_workflow_ids if x is not None]


class DeploymentHistory:
    def __init__(
        self,
        id: str,  # workflow id
        deployed_at: datetime,
    ):
        self.id = id
        self.deployed_at = deployed_at


def create_histories(
    repository_histories: list[RepositoryHistory],
    deployment_histories: list[DeploymentHistory],
) -> list[History]:
    idToDeploymentHistoryMap: dict[str, DeploymentHistory] = {}
    for dh in deployment_histories:
        idToDeploymentHistoryMap[dh.id] = dh

    histories = []
    for rh in repository_histories:
        workflow_id = rh.get_workflow_id()
        matched_dh = (
            idToDeploymentHistoryMap.get(workflow_id)
            if workflow_id is not None
            else None
        )
        histories.append(
            History(
                rh.first_committed_at,
                rh.merged_at,
                matched_dh.deployed_at if matched_dh is not None else None,
            )
        )

    return histories
