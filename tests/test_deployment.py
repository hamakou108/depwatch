from datetime import datetime, timezone
import unittest
from unittest.mock import patch, Mock, MagicMock
from depwatch import deployment


class TestDeployment(unittest.TestCase):
    @patch("depwatch.deployment.Circleci")
    def test_get_deployment_history_returns_correct_result(self, mock_Circleci: Mock):
        mock_circleci = MagicMock()
        mock_circleci.get_pipelines.return_value = [
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
        mock_circleci.get_pipeline_workflow.side_effect = [
            [
                {"stopped_at": "2023-01-01T00:00:00.000Z"},
                {"stopped_at": "2023-01-02T00:00:00.000Z"},
            ],
            [
                {"stopped_at": "2023-01-03T00:00:00.000Z"},
                {"stopped_at": "2023-01-04T00:00:00.000Z"},
            ],
        ]
        mock_Circleci.return_value = mock_circleci

        result = deployment.get_deployment_history("hamakou108/my_project", "main", 100)

        assert len(result) == 2
        assert result[0].deployed_at == datetime(2023, 1, 1, tzinfo=timezone.utc)
        assert result[0].sha == "c76089814e0bb532ff0634634c4f08aeab4692f3"
        assert result[1].deployed_at == datetime(2023, 1, 3, tzinfo=timezone.utc)
        assert result[1].sha == "ee2eeb43810fbb1232f28a82af63ad033314bf2b"

    @patch("depwatch.deployment.Circleci")
    def test_get_deployment_history_skips_pipelines_with_errors(
        self, mock_Circleci: Mock
    ):
        mock_circleci = MagicMock()
        mock_circleci.get_pipelines.return_value = [
            {
                "id": "41a70637-129d-4b4c-b285-5a3576470416",
                "errors": ["error"],
                "vcs": {"revision": "c76089814e0bb532ff0634634c4f08aeab4692f3"},
            }
        ]
        mock_Circleci.return_value = mock_circleci

        result = deployment.get_deployment_history("hamakou108/my_project", "main", 100)

        assert len(result) == 0

    @patch("depwatch.deployment.Circleci")
    def test_get_deployment_history_skips_pipelines_with_no_workflows(
        self, mock_Circleci: Mock
    ):
        mock_circleci = MagicMock()
        mock_circleci.get_pipelines.return_value = [
            {
                "id": "41a70637-129d-4b4c-b285-5a3576470416",
                "errors": [],
                "vcs": {"revision": "c76089814e0bb532ff0634634c4f08aeab4692f3"},
            },
        ]
        mock_circleci.get_pipeline_workflow.return_value = []
        mock_Circleci.return_value = mock_circleci

        result = deployment.get_deployment_history("hamakou108/my_project", "main", 100)

        assert len(result) == 0

    @patch("depwatch.deployment.Circleci")
    def test_get_deployment_history_skips_pipelines_with_no_completed_workflows(
        self, mock_Circleci: Mock
    ):
        mock_circleci = MagicMock()
        mock_circleci.get_pipelines.return_value = [
            {
                "id": "41a70637-129d-4b4c-b285-5a3576470416",
                "errors": [],
                "vcs": {"revision": "c76089814e0bb532ff0634634c4f08aeab4692f3"},
            },
        ]
        mock_circleci.get_pipeline_workflow.return_value = [{"stopped_at": None}]
        mock_Circleci.return_value = mock_circleci

        result = deployment.get_deployment_history("hamakou108/my_project", "main", 100)

        assert len(result) == 0
