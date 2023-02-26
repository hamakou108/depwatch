import os
from datetime import datetime
from pycircleci.api import Api

from deploywatch.history import DeploymentHistory


def get_deployment_history(name: str, base: str, limit: int) -> list[DeploymentHistory]:
    histories = []

    ci = Api(token=os.environ.get('CIRCLECI_ACCESS_TOKEN'), url='https://circleci.com/api')
    user_name, project = name.split('/')
    pipelines = ci.get_project_pipelines(user_name, project, branch=base, paginate=True, limit=limit)

    for p in pipelines:
        if len(p.get('errors')) != 0:
            continue

        workflows = ci.get_pipeline_workflow(p.get('id'))

        stopped_at_list = [w.get('stopped_at') for w in workflows]
        latest_stopped_at = None
        for s in stopped_at_list:
            if s is None:
                continue

            current_stopped_at = datetime.fromisoformat(s)
            if latest_stopped_at is None or current_stopped_at < latest_stopped_at:
                latest_stopped_at = current_stopped_at

        histories.append(DeploymentHistory(latest_stopped_at, p.get('vcs').get('revision')))

    return histories
