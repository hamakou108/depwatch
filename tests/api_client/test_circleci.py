from datetime import datetime, timedelta
import json
import unittest
from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

from requests import HTTPError, Response
from depwatch.api_client.circleci import Circleci

from depwatch.exception import DepwatchException


class TestCircleCI(unittest.TestCase):
    def test___init__(self):
        with patch.dict("os.environ", {"CIRCLECI_ACCESS_TOKEN": "token"}):
            Circleci()

    def test___init__when_token_is_missing(self):
        with patch.dict("os.environ", {"CIRCLECI_ACCESS_TOKEN": ""}):
            with self.assertRaises(DepwatchException):
                Circleci()

    @patch("depwatch.api_client.circleci.requests")
    def test_get_pipelines(self, mock_requests: Mock):
        mock_session = MagicMock()
        mock_session.mount.return_value = None
        mock_session.get.return_value = self._make_get_pipelines_return_value(3)

        mock_requests.Session.return_value = mock_session

        with patch.dict("os.environ", {"CIRCLECI_ACCESS_TOKEN": "token"}):
            circleci = Circleci()
            pipelines = circleci.get_pipelines("hamakou108/my_project", "main")

        assert len(pipelines) == 3
        assert pipelines[0].get("created_at") == "2023-04-13T23:20:47.740Z"
        assert pipelines[1].get("created_at") == "2023-04-12T23:20:47.740Z"
        assert pipelines[2].get("created_at") == "2023-04-11T23:20:47.740Z"

    @patch("depwatch.api_client.circleci.requests")
    def test_get_pipelines_when_limit_is_specified(self, mock_requests: Mock):
        mock_session = MagicMock()
        mock_session.mount.return_value = None
        mock_session.get.side_effect = [
            self._make_get_pipelines_return_value(3),
        ]

        mock_requests.Session.return_value = mock_session

        with patch.dict("os.environ", {"CIRCLECI_ACCESS_TOKEN": "token"}):
            circleci = Circleci()
            pipelines = circleci.get_pipelines("hamakou108/my_project", "main", 2)

        assert len(pipelines) == 2
        assert pipelines[0].get("created_at") == "2023-04-13T23:20:47.740Z"
        assert pipelines[1].get("created_at") == "2023-04-12T23:20:47.740Z"

    @patch("depwatch.api_client.circleci.requests")
    def test_get_pipelines_when_multiple_pages_exist(self, mock_requests: Mock):
        mock_session = MagicMock()
        mock_session.mount.return_value = None
        mock_session.get.side_effect = [
            self._make_get_pipelines_return_value(3, True),
            self._make_get_pipelines_return_value(3),
        ]

        mock_requests.Session.return_value = mock_session

        with patch.dict("os.environ", {"CIRCLECI_ACCESS_TOKEN": "token"}):
            circleci = Circleci()
            pipelines = circleci.get_pipelines("hamakou108/my_project", "main")

        assert len(pipelines) == 6
        assert pipelines[0].get("created_at") == "2023-04-13T23:20:47.740Z"
        assert pipelines[1].get("created_at") == "2023-04-12T23:20:47.740Z"
        assert pipelines[2].get("created_at") == "2023-04-11T23:20:47.740Z"
        assert pipelines[3].get("created_at") == "2023-04-13T23:20:47.740Z"
        assert pipelines[4].get("created_at") == "2023-04-12T23:20:47.740Z"
        assert pipelines[5].get("created_at") == "2023-04-11T23:20:47.740Z"

    @patch("depwatch.api_client.circleci.requests")
    def test_get_pipelines_when_project_is_not_found(self, mock_requests: Mock):
        mock_session = MagicMock()
        mock_session.mount.return_value = None
        mock_session.get.return_value = (
            self._make_get_pipelines_return_value_when_project_is_not_found()
        )

        mock_requests.Session.return_value = mock_session

        with patch.dict("os.environ", {"CIRCLECI_ACCESS_TOKEN": "token"}):
            circleci = Circleci()
            with self.assertRaises(DepwatchException):
                circleci.get_pipelines("hamakou108/my_project", "main")

    @patch("depwatch.api_client.circleci.requests")
    def test_get_pipeline_workflows(self, mock_requests: Mock):
        mock_session = MagicMock()
        mock_session.mount.return_value = None
        mock_session.get.return_value = self._make_get_pipeline_workflows_return_value(
            3
        )

        mock_requests.Session.return_value = mock_session

        with patch.dict("os.environ", {"CIRCLECI_ACCESS_TOKEN": "token"}):
            circleci = Circleci()
            workflows = circleci.get_pipeline_workflow("pipeline_id")

        assert len(workflows) == 3
        assert workflows[0].get("created_at") == "2023-04-13T23:20:47.740Z"
        assert workflows[1].get("created_at") == "2023-04-12T23:20:47.740Z"
        assert workflows[2].get("created_at") == "2023-04-11T23:20:47.740Z"

    @patch("depwatch.api_client.circleci.requests")
    def test_get_pipeline_workflows_when_multiple_pages_exist(
        self, mock_requests: Mock
    ):
        mock_session = MagicMock()
        mock_session.mount.return_value = None
        mock_session.get.return_value = self._make_get_pipeline_workflows_return_value(
            3
        )

        mock_requests.Session.return_value = mock_session

        with patch.dict("os.environ", {"CIRCLECI_ACCESS_TOKEN": "token"}):
            circleci = Circleci()
            workflows = circleci.get_pipeline_workflow("pipeline_id")

        assert len(workflows) == 3
        assert workflows[0].get("created_at") == "2023-04-13T23:20:47.740Z"
        assert workflows[1].get("created_at") == "2023-04-12T23:20:47.740Z"
        assert workflows[2].get("created_at") == "2023-04-11T23:20:47.740Z"

    @patch("depwatch.api_client.circleci.requests")
    def test_get_pipeline_workflows_when_workflows_not_found(self, mock_requests: Mock):
        mock_session = MagicMock()
        mock_session.mount.return_value = None
        # Access to workflows that are over six months old is deleted (?) on CircleCI
        response_404 = Response()
        response_404.status_code = 404
        mock_session.get.side_effect = HTTPError(response=response_404)

        mock_requests.Session.return_value = mock_session

        with patch.dict("os.environ", {"CIRCLECI_ACCESS_TOKEN": "token"}):
            circleci = Circleci()
            workflows = circleci.get_pipeline_workflow("pipeline_id")

        assert len(workflows) == 0

    def _make_get_pipelines_return_value(self, num: int, has_next_page: bool = False):
        items = []

        for n in range(num):
            base_datetime = datetime(2023, 4, 13, 23, 20, 47, 740000)
            updated_at = base_datetime - timedelta(days=n)
            created_at = base_datetime - timedelta(days=n)
            received_at = base_datetime - timedelta(days=n)

            items.append(
                {
                    "id": uuid4().__str__(),
                    "errors": [],
                    "project_slug": "gh/hamakou108/my-project",
                    "updated_at": updated_at.isoformat(timespec="milliseconds") + "Z",
                    "number": num - n,
                    "state": "created",
                    "created_at": created_at.isoformat(timespec="milliseconds") + "Z",
                    "trigger": {
                        "received_at": received_at.isoformat(timespec="milliseconds")
                        + "Z",
                        "type": "webhook",
                        "actor": {
                            "login": "hamakou108",
                            "avatar_url": "https://avatars.githubusercontent.com/u/19360521?v=4",
                        },
                    },
                    "vcs": {
                        "origin_repository_url": "https://github.com/hamakou108/my-project",
                        "target_repository_url": "https://github.com/hamakou108/my-project",
                        "revision": "9638b4160428ddd0d184e4fccc29df6b72e289c0",
                        "provider_name": "GitHub",
                        "commit": {
                            "body": "Pull Request Title",
                            "subject": "Merge pull request #1 from macloud-developer/feature-branch",
                        },
                        "branch": "main",
                    },
                }
            )

        res_content = {
            "next_page_token": "dummy" if has_next_page else None,
            "items": items,
        }

        res = Response()
        res.status_code = 200
        res.headers["content-type"] = "application/json"
        res.encoding = "utf-8"
        res._content = bytes(json.dumps(res_content), "utf-8")
        return res

    def _make_get_pipelines_return_value_when_project_is_not_found(self):
        res_content = {"message": "Project not found"}
        res = Response()
        res.status_code = 404
        res.headers["content-type"] = "application/json"
        res.encoding = "utf-8"
        res._content = bytes(json.dumps(res_content), "utf-8")
        return res

    def _make_get_pipeline_workflows_return_value(self, num):
        items = []

        for n in range(num):
            base_datetime = datetime(2023, 4, 13, 23, 20, 47, 740000)
            created_at = base_datetime - timedelta(days=n)
            stopped_at = base_datetime - timedelta(days=n) + timedelta(minutes=30)

            items.append(
                {
                    "pipeline_id": uuid4().__str__(),
                    "id": uuid4().__str__(),
                    "name": "workflow-name",
                    "project_slug": "gh/hamakou108/my-project",
                    "status": "success",
                    "started_by": uuid4().__str__(),
                    "pipeline_number": 1,
                    "created_at": created_at.isoformat(timespec="milliseconds") + "Z",
                    "stopped_at": stopped_at.isoformat(timespec="milliseconds") + "Z",
                }
            )

        res_content = {
            "next_page_token": None,
            "items": items,
        }

        res = Response()
        res.status_code = 200
        res.headers["content-type"] = "application/json"
        res.encoding = "utf-8"
        res._content = bytes(json.dumps(res_content), "utf-8")
        return res
