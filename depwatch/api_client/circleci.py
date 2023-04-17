import os
from typing import cast
import requests
from requests import HTTPError
from depwatch.exception import DepwatchException


class Circleci:
    def __init__(self):
        token = os.environ.get("CIRCLECI_ACCESS_TOKEN")
        if not token:
            raise DepwatchException("Missing CircleCI API token")

        self.headers = {
            "Accept": "application/json",
            "Circle-Token": token,
        }

    def get_pipelines(
        self,
        name: str,
        branch: str,
        limit: int | None = None,
    ) -> list[dict]:
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        session.mount("https://", adapter)

        items = []
        next_page_token: str = ""
        while True:
            queryParamsString = (
                f"?page-token={next_page_token}" if next_page_token else ""
            )
            res = session.get(
                f"https://circleci.com/api/v2/project/gh/{name}/pipeline{queryParamsString}",
                params={"branch": branch},
                headers=self.headers,
            )

            # Occurs when the Project is not found (maybe bad credentials)
            if res.status_code == 404:
                raise DepwatchException(res.content)

            items += res.json().get("items")

            if limit is not None and len(items) >= limit:
                items = items[:limit]
                break

            next_page_token = res.json().get("next_page_token")
            if not next_page_token:
                break

        return items

    def get_pipeline_workflow(
        self,
        pipeline_id: str,
    ) -> list[dict]:
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        session.mount("https://", adapter)

        try:
            res = session.get(
                f"https://circleci.com/api/v2/pipeline/{pipeline_id}/workflow",
                headers=self.headers,
            )
        except HTTPError as e:
            if cast(requests.Response, e.response).status_code == 404:
                return []
            else:
                raise e

        return res.json().get("items")
