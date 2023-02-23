from command import History, generate_histories

from datetime import datetime


def test_history():
    expected = [
        History(
            datetime.fromisoformat('2023-02-23T10:00:00+00:00'),
            datetime.fromisoformat('2023-02-23T11:00:00+00:00'),
            datetime.fromisoformat('2023-02-23T11:30:00+00:00'),
        )
    ]

    assert generate_histories() == expected
