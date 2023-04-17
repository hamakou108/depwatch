from datetime import datetime
from typing import Sized
from depwatch.api_client.circleci import Circleci
from depwatch.exception import DepwatchException
from depwatch.history import DeploymentHistory


def get_deployment_history(name: str, base: str, limit: int) -> list[DeploymentHistory]:
    histories = []

    circleci = Circleci()
    pipelines = circleci.get_pipelines(name, base, limit)

    for p in pipelines:
        errors = p.get("errors")
        if not isinstance(errors, Sized):
            raise DepwatchException('Unexpected type of the field "error"')

        if len(errors) != 0:
            continue

        id = p.get("id")
        if not isinstance(id, str):
            raise DepwatchException('Unexpected type of the field "id"')

        workflows = circleci.get_pipeline_workflow(id)

        stopped_at_list = [w.get("stopped_at") for w in workflows]
        latest_stopped_at = None
        for s in stopped_at_list:
            if s is None:
                continue

            current_stopped_at = datetime.fromisoformat(s)
            if latest_stopped_at is None or current_stopped_at < latest_stopped_at:
                latest_stopped_at = current_stopped_at

        if latest_stopped_at is None:
            continue

        vcs = p.get("vcs")
        if not isinstance(vcs, dict):
            raise DepwatchException('Unexpected type of the field "vcs"')

        revision = vcs.get("revision")
        if not isinstance(revision, str):
            raise DepwatchException('Unexpected type of the field "revision"')

        histories.append(DeploymentHistory(latest_stopped_at, revision))

    return histories
