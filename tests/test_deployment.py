from datetime import datetime, timezone
from unittest.mock import patch, Mock, MagicMock

from requests import HTTPError, Response
from depwatch import deployment

utc = timezone.utc


class TestDeployment:
    @patch("depwatch.deployment.Api")
    def test_get_deployment_history(self, mock_Api: Mock):
        mock_ci = MagicMock()
        mock_ci.get_workflow.side_effect = [
            {
                "id": "40020909-fd66-4657-b3e4-8872627507d2",
                "status": "success",
                "stopped_at": "2023-01-01T00:00:00.000Z",
            },
            {
                "id": "84abef06-1fa2-48ec-875e-382e9b7add78",
                "status": "success",
                "stopped_at": "2023-01-02T00:00:00.000Z",
            },
        ]
        mock_Api.return_value = mock_ci

        workflow_ids = [
            "40020909-fd66-4657-b3e4-8872627507d2",
            "84abef06-1fa2-48ec-875e-382e9b7add78",
        ]
        result = deployment.get_deployment_history(workflow_ids)

        assert len(result) == 2
        assert result[0].id == "40020909-fd66-4657-b3e4-8872627507d2"
        assert result[0].deployed_at == datetime(2023, 1, 1, tzinfo=timezone.utc)
        assert result[1].id == "84abef06-1fa2-48ec-875e-382e9b7add78"
        assert result[1].deployed_at == datetime(2023, 1, 2, tzinfo=timezone.utc)

    # Access to pipelines that are over six months old is not available on CircleCI
    @patch("depwatch.deployment.Api")
    def test_get_deployment_history_when_the_workflow_has_removed_then_the_item_is_not_appended(
        self, mock_Api: Mock
    ):
        mock_ci = MagicMock()
        response_404 = Response()
        response_404.status_code = 404
        mock_ci.get_workflow.side_effect = HTTPError(response=response_404)
        mock_Api.return_value = mock_ci

        workflow_ids = [
            "40020909-fd66-4657-b3e4-8872627507d2",
        ]
        result = deployment.get_deployment_history(workflow_ids)

        assert len(result) == 0

    @patch("depwatch.deployment.Api")
    def test_get_deployment_history_when_the_workflow_has_not_been_completed_then_the_item_is_not_appended(
        self, mock_Api: Mock
    ):
        mock_ci = MagicMock()
        mock_ci.get_workflow.return_value = {
            "id": "40020909-fd66-4657-b3e4-8872627507d2",
            "status": "success",
            "stopped_at": None,
        }
        mock_Api.return_value = mock_ci

        workflow_ids = [
            "40020909-fd66-4657-b3e4-8872627507d2",
        ]
        result = deployment.get_deployment_history(workflow_ids)

        assert len(result) == 0

    @patch("depwatch.deployment.Api")
    def test_get_deployment_history_when_the_workflow_is_not_successful_then_the_item_is_not_appended(
        self, mock_Api: Mock
    ):
        mock_ci = MagicMock()
        mock_ci.get_workflow.return_value = {
            "id": "40020909-fd66-4657-b3e4-8872627507d2",
            "status": "failed",
            "stopped_at": "2023-01-01T00:00:00.000Z",
        }
        mock_Api.return_value = mock_ci

        workflow_ids = [
            "40020909-fd66-4657-b3e4-8872627507d2",
        ]
        result = deployment.get_deployment_history(workflow_ids)

        assert len(result) == 0
