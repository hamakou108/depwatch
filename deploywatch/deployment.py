import os
from datetime import datetime
from pycircleci.api import Api


class DeploymentHistory:
    def __init__(
            self,
            deployed_at: datetime,
    ):
        self.deployed_at = deployed_at


def get_deployment_history(name: str, sha_list: list) -> list[DeploymentHistory]:
    histories = []

    ci = Api(token=os.environ.get('CIRCLECI_ACCESS_TOKEN'), url='https://circleci.com/api')
    user_name, project = name.split('/')
    pipelines = ci.get_project_pipelines(user_name, project)

    for p in pipelines:
        if len(p.get('errors')) != 0:
            continue

        for sha in sha_list:
            workflows = None
            if p.get('vcs').get('revision') == sha:
                workflows = ci.get_pipeline_workflow(p.get('id'))

            if workflows is None:
                continue

            stopped_at_list = [w.get('stopped_at') for w in workflows]
            latest_stopped_at = None
            for s in stopped_at_list:
                if s is None:
                    continue

                current_stopped_at = datetime.fromisoformat(s)
                if latest_stopped_at is None or current_stopped_at < latest_stopped_at:
                    latest_stopped_at = current_stopped_at

            histories.append(DeploymentHistory(latest_stopped_at))

    return histories
