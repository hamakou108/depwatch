from deploywatch import command
from deploywatch.command import Scope, History, generate_histories
from deploywatch.repository import RepositoryHistory

from datetime import datetime


def fake_get_repository_history(name: str):
    return [
        RepositoryHistory(
            datetime.fromisoformat('2023-02-23T10:00:00+00:00'),
            datetime.fromisoformat('2023-02-23T11:00:00+00:00')
        ),
        RepositoryHistory(
            datetime.fromisoformat('2023-02-23T10:05:00+00:00'),
            datetime.fromisoformat('2023-02-23T11:15:00+00:00'),
        ),
    ]


def test_generate_histories(mocker):
    mocker.patch.object(command, 'get_repository_history', fake_get_repository_history)

    expected = [
        History(
            datetime.fromisoformat('2023-02-23T10:00:00+00:00'),
            datetime.fromisoformat('2023-02-23T11:00:00+00:00'),
            datetime.fromisoformat('2023-02-23T11:30:00+00:00'),
        ),
        History(
            datetime.fromisoformat('2023-02-23T10:05:00+00:00'),
            datetime.fromisoformat('2023-02-23T11:15:00+00:00'),
            datetime.fromisoformat('2023-02-23T11:30:00+00:00'),
        ),
    ]

    assert generate_histories('foo', Scope('all')) == expected
