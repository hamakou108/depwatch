import os
from datetime import datetime
from pycircleci.api import Api
from requests import HTTPError
from requests.models import Response
from typing import cast

from depwatch.history import DeploymentHistory


def get_deployment_history(workflow_ids: list[str]) -> list[DeploymentHistory]:
    def __get_workflow(id):
        try:
            return ci.get_workflow(id)
        except HTTPError as e:
            if cast(Response, e.response).status_code == 404:
                return []
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
        workflows = __get_workflow(id)
        succeeded_workflows = filter(__is_succeeded_workflows, workflows)

        first_succeeded_workflow = None
        for w in succeeded_workflows:
            if first_succeeded_workflow is None:
                first_succeeded_workflow = w
                continue

            if datetime.fromisoformat(w.get("stopped_at")) < datetime.fromisoformat(
                first_succeeded_workflow.get("stopped_at")
            ):
                first_succeeded_workflow = w

        if first_succeeded_workflow is None:
            continue

        histories.append(
            DeploymentHistory(
                first_succeeded_workflow.get("id"),
                datetime.fromisoformat(first_succeeded_workflow.get("stopped_at")),
            )
        )

    return histories
