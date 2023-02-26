from unittest.mock import patch, Mock

from deploywatch import command
from deploywatch.command import generate_histories
from deploywatch.history import History, RepositoryHistory, DeploymentHistory

from datetime import datetime


class TestCommand:
    @patch.object(command, 'write_histories')
    @patch.object(command, 'get_deployment_history', return_value=[])
    @patch.object(command, 'get_repository_history', return_value=[])
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
