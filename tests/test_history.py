from datetime import datetime
from depwatch.history import (
    DeploymentHistory,
    History,
    RepositoryHistory,
    create_histories,
)


class TestHistory:
    def test_create_histories(self):
        repository_histories = [
            RepositoryHistory(
                datetime.fromisoformat("2023-02-25T20:00:00+00:00"),
                datetime.fromisoformat("2023-02-26T22:00:00+00:00"),
                "8eddb4b87a1460b29bce25448623b270465e9715",
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-02-23T10:05:00+00:00"),
                datetime.fromisoformat("2023-02-23T11:15:00+00:00"),
                "12d4c5f2a123b6fb77eccb57be1be3a29438fadb",
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-02-23T10:00:00+00:00"),
                datetime.fromisoformat("2023-02-23T11:00:00+00:00"),
                "cbd1519fd8b7daff2655346676065f844a2ef3df",
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-02-22T14:00:00+00:00"),
                datetime.fromisoformat("2023-02-22T17:00:00+00:00"),
                "b25ab2d8590fc678ced72fe378c0bf2dc04da15c",
            ),
        ]
        deployment_histories = [
            DeploymentHistory(
                datetime.fromisoformat("2023-02-27T10:15:00+00:00"),
                "8eddb4b87a1460b29bce25448623b270465e9715",
            ),
            DeploymentHistory(
                datetime.fromisoformat("2023-02-24T09:30:00+00:00"),
                "b25ab2d8590fc678ced72fe378c0bf2dc04da15c",
            ),
            DeploymentHistory(
                datetime.fromisoformat("2023-02-23T11:30:00+00:00"),
                "12d4c5f2a123b6fb77eccb57be1be3a29438fadb",
            ),
        ]

        histories = create_histories(repository_histories, deployment_histories)

        assert histories == [
            History(
                datetime.fromisoformat("2023-02-25T20:00:00+00:00"),
                datetime.fromisoformat("2023-02-26T22:00:00+00:00"),
                datetime.fromisoformat("2023-02-27T10:15:00+00:00"),
            ),
            History(
                datetime.fromisoformat("2023-02-23T10:05:00+00:00"),
                datetime.fromisoformat("2023-02-23T11:15:00+00:00"),
                datetime.fromisoformat("2023-02-23T11:30:00+00:00"),
            ),
            History(
                datetime.fromisoformat("2023-02-23T10:00:00+00:00"),
                datetime.fromisoformat("2023-02-23T11:00:00+00:00"),
                None,
            ),
            History(
                datetime.fromisoformat("2023-02-22T14:00:00+00:00"),
                datetime.fromisoformat("2023-02-22T17:00:00+00:00"),
                datetime.fromisoformat("2023-02-24T09:30:00+00:00"),
            ),
        ]
