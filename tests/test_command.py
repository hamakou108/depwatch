from unittest.mock import patch, Mock

from deploywatch import command
from deploywatch.command import generate_histories
from deploywatch.history import History, RepositoryHistory, DeploymentHistory

from datetime import datetime


class TestCommand:
    @patch.object(command, 'write_histories')
    @patch.object(command, 'get_deployment_history', return_value=[
        DeploymentHistory(
            datetime.fromisoformat('2023-02-27T10:15:00+00:00'),
            '8eddb4b87a1460b29bce25448623b270465e9715',
        ),
        DeploymentHistory(
            datetime.fromisoformat('2023-02-23T11:30:00+00:00'),
            '12d4c5f2a123b6fb77eccb57be1be3a29438fadb',
        ),
    ])
    @patch.object(command, 'get_repository_history', return_value=[
        RepositoryHistory(
            datetime.fromisoformat('2023-02-25T20:00:00+00:00'),
            datetime.fromisoformat('2023-02-26T22:00:00+00:00'),
            '8eddb4b87a1460b29bce25448623b270465e9715',
        ),
        RepositoryHistory(
            datetime.fromisoformat('2023-02-23T10:05:00+00:00'),
            datetime.fromisoformat('2023-02-23T11:15:00+00:00'),
            '12d4c5f2a123b6fb77eccb57be1be3a29438fadb',
        ),
        RepositoryHistory(
            datetime.fromisoformat('2023-02-23T10:00:00+00:00'),
            datetime.fromisoformat('2023-02-23T11:00:00+00:00'),
            'cbd1519fd8b7daff2655346676065f844a2ef3df',
        ),
    ])
    @patch.object(command, 'get_main_branch', return_value='main')
    def test_generate_histories(
            self,
            get_main_branch_mock: Mock,
            get_repository_history_mock: Mock,
            get_deployment_history_mock: Mock,
            write_histories_mock: Mock,
    ):
        generate_histories('hamakou108/my_project', False, 100)

        get_main_branch_mock.assert_called_once_with('hamakou108/my_project')
        get_repository_history_mock.assert_called_once_with('hamakou108/my_project', 'main', 100)
        get_deployment_history_mock.assert_called_once_with('hamakou108/my_project', 'main', 100)
        write_histories_mock.assert_called()

    @patch.object(command, 'write_histories')
    @patch.object(command, 'get_deployment_history', return_value=[])
    @patch.object(command, 'get_repository_history', return_value=[])
    @patch.object(command, 'get_main_branch', return_value='main')
    def test_generate_histories_with_code_only(
            self,
            get_main_branch_mock: Mock,
            get_repository_history_mock: Mock,
            get_deployment_history_mock: Mock,
            write_histories_mock: Mock,
    ):
        generate_histories('hamakou108/my_project', True, 100)

        get_deployment_history_mock.assert_not_called()
