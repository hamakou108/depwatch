import os
from datetime import datetime
from pycircleci.api import Api
from requests import HTTPError
from requests.models import Response
from typing import cast
from depwatch.exception import DepwatchException

from depwatch.history import DeploymentHistory


def get_deployment_history(workflow_ids: list[str]) -> list[DeploymentHistory]:
    def __get_workflow(id):
        try:
            return ci.get_workflow(id)
        except HTTPError as e:
            if cast(Response, e.response).status_code == 404:
                raise DepwatchException("The workflow is not found")
            else:
                raise e

    def __is_succeeded_workflows(workflow) -> bool:
        return (
            workflow.get("status") == "success"
            and workflow.get("stopped_at") is not None
        )

    histories = []

    ci = Api(
        token=os.environ.get("CIRCLECI_ACCESS_TOKEN"), url="https://circleci.com/api"
    )

    for id in workflow_ids:
        try:
            workflow = __get_workflow(id)
        except DepwatchException:
            continue

        if not __is_succeeded_workflows(workflow):
            continue

        histories.append(
            DeploymentHistory(
                workflow.get("id"),
                datetime.fromisoformat(workflow.get("stopped_at")),
            )
        )

    return histories
