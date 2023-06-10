from datetime import datetime
import json
from typing import Optional


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
        check_runs: list,
    ):
        self.first_committed_at = first_committed_at
        self.merged_at = merged_at
        self.merge_commit_sha = merge_commit_sha
        self.check_runs = check_runs

    def __get_target_check_run(self, name: str | None = None) -> dict | None:
        if name is None:
            return self.check_runs[0]

        try:
            return next(cr for cr in self.check_runs if cr["name"] == name)
        except StopIteration:
            return None

    def get_workflow_id(self, name: str | None = None) -> str | None:
        if len(self.check_runs) == 0:
            return None

        check_run = self.__get_target_check_run(name)

        if check_run is None:
            return None

        if check_run["app"]["slug"] != "circleci-checks":
            return None

        decoded_external_id = json.loads(check_run["external_id"])

        return decoded_external_id["workflow-id"]


def convert_repository_history_to_workflow_ids(
    repository_histories: list[RepositoryHistory], workflow_name: str | None = None
) -> list[str]:
    raw_workflow_ids = [
        history.get_workflow_id(workflow_name) for history in repository_histories
    ]
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
    workflow_name: str | None = None,
) -> list[History]:
    idToDeploymentHistoryMap: dict[str, DeploymentHistory] = {}
    for dh in deployment_histories:
        idToDeploymentHistoryMap[dh.id] = dh

    histories = []
    for rh in repository_histories:
        workflow_id = rh.get_workflow_id(workflow_name)
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
