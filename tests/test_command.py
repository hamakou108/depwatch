from deploywatch import command
from deploywatch.command import History, generate_histories
from deploywatch.repository import RepositoryHistory
from deploywatch.deployment import DeploymentHistory

from datetime import datetime


def fake_get_repository_history(name: str):
    return [
        RepositoryHistory(
            datetime.fromisoformat('2023-02-23T10:00:00+00:00'),
            datetime.fromisoformat('2023-02-23T11:00:00+00:00'),
            'cbd1519fd8b7daff2655346676065f844a2ef3df',
        ),
        RepositoryHistory(
            datetime.fromisoformat('2023-02-23T10:05:00+00:00'),
            datetime.fromisoformat('2023-02-23T11:15:00+00:00'),
            '12d4c5f2a123b6fb77eccb57be1be3a29438fadb',
        ),
    ]


def fake_get_deployment_history(name: str, sha_list: list):
    return [
        DeploymentHistory(
            datetime.fromisoformat('2023-02-23T11:15:00+00:00'),
        ),
        DeploymentHistory(
            datetime.fromisoformat('2023-02-23T11:30:00+00:00'),
        ),
    ]


class TestCommand:
    def test_generate_histories(self, mocker):
        mocker.patch.object(command, 'get_repository_history', fake_get_repository_history)
        mocker.patch.object(command, 'get_deployment_history', fake_get_deployment_history)

        expected = [
            History(
                datetime.fromisoformat('2023-02-23T10:00:00+00:00'),
                datetime.fromisoformat('2023-02-23T11:00:00+00:00'),
                datetime.fromisoformat('2023-02-23T11:15:00+00:00'),
            ),
            History(
                datetime.fromisoformat('2023-02-23T10:05:00+00:00'),
                datetime.fromisoformat('2023-02-23T11:15:00+00:00'),
                datetime.fromisoformat('2023-02-23T11:30:00+00:00'),
            ),
        ]

        assert generate_histories('foo', False) == expected
