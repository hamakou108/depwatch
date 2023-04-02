from datetime import datetime, timezone
from unittest.mock import patch, Mock, MagicMock

from requests import HTTPError, Response
from depwatch import deployment

utc = timezone.utc


class TestDeployment:
    @patch("depwatch.deployment.Api")
    def test_get_deployment_history_returns_correct_result(self, mock_Api: Mock):
        mock_ci = MagicMock()
        mock_ci.get_project_pipelines.return_value = [
            {
                "id": "41a70637-129d-4b4c-b285-5a3576470416",
                "errors": [],
                "vcs": {"revision": "c76089814e0bb532ff0634634c4f08aeab4692f3"},
            },
            {
                "id": "da6b8e0d-b3f2-49f4-91d1-9031426f9213",
                "errors": [],
                "vcs": {"revision": "ee2eeb43810fbb1232f28a82af63ad033314bf2b"},
            },
        ]
        mock_ci.get_pipeline_workflow.side_effect = [
            [
                {"stopped_at": "2023-01-01T00:00:00.000Z"},
                {"stopped_at": "2023-01-02T00:00:00.000Z"},
            ],
            [
                {"stopped_at": "2023-01-01T00:00:00.000Z"},
                {"stopped_at": "2023-01-02T00:00:00.000Z"},
            ],
            [
                {"stopped_at": "2023-01-03T00:00:00.000Z"},
                {"stopped_at": "2023-01-04T00:00:00.000Z"},
            ],
            [
                {"stopped_at": "2023-01-03T00:00:00.000Z"},
                {"stopped_at": "2023-01-04T00:00:00.000Z"},
            ],
        ]
        mock_Api.return_value = mock_ci

        result = deployment.get_deployment_history("hamakou108/my_project", "main", 100)

        assert len(result) == 2
        assert result[0].deployed_at == datetime(2023, 1, 1, tzinfo=timezone.utc)
        assert result[0].sha == "c76089814e0bb532ff0634634c4f08aeab4692f3"
        assert result[1].deployed_at == datetime(2023, 1, 3, tzinfo=timezone.utc)
        assert result[1].sha == "ee2eeb43810fbb1232f28a82af63ad033314bf2b"

    @patch("depwatch.deployment.Api")
    def test_get_deployment_history_skips_pipelines_with_errors(self, mock_Api: Mock):
        mock_ci = MagicMock()
        mock_ci.get_project_pipelines.return_value = [
            {
                "id": "41a70637-129d-4b4c-b285-5a3576470416",
                "errors": ["error"],
                "vcs": {"revision": "c76089814e0bb532ff0634634c4f08aeab4692f3"},
            }
        ]
        mock_Api.return_value = mock_ci

        result = deployment.get_deployment_history("hamakou108/my_project", "main", 100)

        assert len(result) == 0

    # Access to pipelines that are over six months old is not available on CircleCI
    @patch("depwatch.deployment.Api")
    def test_get_deployment_history_skips_pipelines_with_pipeline_has_removed(
        self, mock_Api: Mock
    ):
        mock_ci = MagicMock()
        mock_ci.get_project_pipelines.return_value = [
            {
                "id": "41a70637-129d-4b4c-b285-5a3576470416",
                "errors": [],
                "vcs": {"revision": "c76089814e0bb532ff0634634c4f08aeab4692f3"},
            }
        ]
        response_404 = Response()
        response_404.status_code = 404
        mock_ci.get_pipeline_workflow.side_effect = HTTPError(response=response_404)
        mock_Api.return_value = mock_ci

        result = deployment.get_deployment_history("hamakou108/my_project", "main", 100)

        assert len(result) == 0

    @patch("depwatch.deployment.Api")
    def test_get_deployment_history_skips_pipelines_with_no_workflows(
        self, mock_Api: Mock
    ):
        mock_ci = MagicMock()
        mock_ci.get_project_pipelines.return_value = [
            {
                "id": "41a70637-129d-4b4c-b285-5a3576470416",
                "errors": [],
                "vcs": {"revision": "c76089814e0bb532ff0634634c4f08aeab4692f3"},
            },
        ]
        mock_ci.get_pipeline_workflow.return_value = []
        mock_Api.return_value = mock_ci

        result = deployment.get_deployment_history("hamakou108/my_project", "main", 100)

        assert len(result) == 0

    @patch("depwatch.deployment.Api")
    def test_get_deployment_history_skips_pipelines_with_no_completed_workflows(
        self, mock_Api: Mock
    ):
        mock_ci = MagicMock()
        mock_ci.get_project_pipelines.return_value = [
            {
                "id": "41a70637-129d-4b4c-b285-5a3576470416",
                "errors": [],
                "vcs": {"revision": "c76089814e0bb532ff0634634c4f08aeab4692f3"},
            },
        ]
        mock_ci.get_pipeline_workflow.return_value = [{"stopped_at": None}]
        mock_Api.return_value = mock_ci

        result = deployment.get_deployment_history("hamakou108/my_project", "main", 100)

        assert len(result) == 0
