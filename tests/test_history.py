from datetime import datetime
from depwatch.exception import DepwatchException
from depwatch.history import (
    DeploymentHistory,
    History,
    RepositoryHistory,
    convert_repository_history_to_workflow_ids,
    create_histories,
)


class TestHistory:
    def test_repository_history_get_workflow_id(self) -> None:
        rh = RepositoryHistory(
            datetime.fromisoformat("2023-04-26T20:00:00+00:00"),
            datetime.fromisoformat("2023-04-26T22:00:00+00:00"),
            "b30000653abd86ff77b2a3e59b427896f4b16ccf",
            "circleci-checks",
            '{"workflow-id":"72d1d896-cfbe-48e2-a023-51edb6438b9f","actor-id":"5ead47d7-6407-4264-a150-7f68b8c98631"}',
        )

        assert rh.get_workflow_id() == "72d1d896-cfbe-48e2-a023-51edb6438b9f"

    def test_repository_history_get_workflow_id_when_check_run_is_not_provided(
        self,
    ) -> None:
        rh = RepositoryHistory(
            datetime.fromisoformat("2023-04-26T20:00:00+00:00"),
            datetime.fromisoformat("2023-04-26T22:00:00+00:00"),
            "b30000653abd86ff77b2a3e59b427896f4b16ccf",
        )

        assert rh.get_workflow_id() == None

    def test_repository_history_get_workflow_id_when_the_check_run_app_slug_is_not_supported(
        self,
    ) -> None:
        rh = RepositoryHistory(
            datetime.fromisoformat("2023-04-26T20:00:00+00:00"),
            datetime.fromisoformat("2023-04-26T22:00:00+00:00"),
            "b30000653abd86ff77b2a3e59b427896f4b16ccf",
            "custom-checks",
            '{"foo":"bar"}',
        )

        assert rh.get_workflow_id() == None

    def test_repository_history_get_workflow_id_when_check_run_external_id_is_not_provided(
        self,
    ) -> None:
        rh = RepositoryHistory(
            datetime.fromisoformat("2023-04-26T20:00:00+00:00"),
            datetime.fromisoformat("2023-04-26T22:00:00+00:00"),
            "b30000653abd86ff77b2a3e59b427896f4b16ccf",
            "circleci-checks",
        )

        try:
            rh.get_workflow_id()
            assert False
        except DepwatchException as e:
            assert str(e) == "'check_run.external_id' was not found"

    def test_convert_repository_history_to_workflow_ids(self) -> None:
        repository_histories = [
            RepositoryHistory(
                datetime.fromisoformat("2023-04-26T20:00:00+00:00"),
                datetime.fromisoformat("2023-04-26T22:00:00+00:00"),
                "b30000653abd86ff77b2a3e59b427896f4b16ccf",
                "circleci-checks",
                '{"workflow-id":"72d1d896-cfbe-48e2-a023-51edb6438b9f","actor-id":"5ead47d7-6407-4264-a150-7f68b8c98631"}',
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-04-25T20:00:00+00:00"),
                datetime.fromisoformat("2023-04-25T22:00:00+00:00"),
                "cebc0584d4ebeb2da4ed488be5d02c9ca2c7efeb",
                "circleci-checks",
                '{"workflow-id":"da5718a4-d796-4414-a6f7-bb3b26c01bf8","actor-id":"33a61365-e7ef-453c-a105-4aa8d342ca8e"}',
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-04-24T20:00:00+00:00"),
                datetime.fromisoformat("2023-04-24T22:00:00+00:00"),
                "a6a8e9e33c0854dc742f03e0c48977cad1cec72f",
                "circleci-checks",
                '{"workflow-id":"20219ed8-6bce-4760-9b7c-b50d2eb34099","actor-id":"18b815e9-4438-4fba-b65c-77b224ecc116"}',
            ),
        ]

        pipeline_list = convert_repository_history_to_workflow_ids(repository_histories)

        assert pipeline_list == [
            "72d1d896-cfbe-48e2-a023-51edb6438b9f",
            "da5718a4-d796-4414-a6f7-bb3b26c01bf8",
            "20219ed8-6bce-4760-9b7c-b50d2eb34099",
        ]

    def test_convert_repository_history_to_workflow_ids_when_a_item_not_having_workflow_id_is_included(
        self,
    ) -> None:
        repository_histories = [
            RepositoryHistory(
                datetime.fromisoformat("2023-04-26T20:00:00+00:00"),
                datetime.fromisoformat("2023-04-26T22:00:00+00:00"),
                "b30000653abd86ff77b2a3e59b427896f4b16ccf",
                "circleci-checks",
                '{"workflow-id":"72d1d896-cfbe-48e2-a023-51edb6438b9f","actor-id":"5ead47d7-6407-4264-a150-7f68b8c98631"}',
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-04-25T20:00:00+00:00"),
                datetime.fromisoformat("2023-04-25T22:00:00+00:00"),
                "cebc0584d4ebeb2da4ed488be5d02c9ca2c7efeb",
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-04-24T20:00:00+00:00"),
                datetime.fromisoformat("2023-04-24T22:00:00+00:00"),
                "a6a8e9e33c0854dc742f03e0c48977cad1cec72f",
                "circleci-checks",
                '{"workflow-id":"20219ed8-6bce-4760-9b7c-b50d2eb34099","actor-id":"18b815e9-4438-4fba-b65c-77b224ecc116"}',
            ),
        ]

        pipeline_list = convert_repository_history_to_workflow_ids(repository_histories)

        assert pipeline_list == [
            "72d1d896-cfbe-48e2-a023-51edb6438b9f",
            "20219ed8-6bce-4760-9b7c-b50d2eb34099",
        ]

    def test_create_histories(self):
        repository_histories = [
            RepositoryHistory(
                datetime.fromisoformat("2023-02-25T20:00:00+00:00"),
                datetime.fromisoformat("2023-02-26T22:00:00+00:00"),
                "8eddb4b87a1460b29bce25448623b270465e9715",
                "circleci-checks",
                '{"workflow-id":"52166f56-7e17-40f5-b7dd-5e8c55d388a8","actor-id":"18b815e9-4438-4fba-b65c-77b224ecc116"}',
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-02-23T10:05:00+00:00"),
                datetime.fromisoformat("2023-02-23T11:15:00+00:00"),
                "12d4c5f2a123b6fb77eccb57be1be3a29438fadb",
                "circleci-checks",
                '{"workflow-id":"b609a9ab-92f2-46b2-b1c2-a9e9b9f3ffc7","actor-id":"58f32647-4d45-4b93-9b57-e9712de5ce08"}',
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-02-23T10:00:00+00:00"),
                datetime.fromisoformat("2023-02-23T11:00:00+00:00"),
                "cbd1519fd8b7daff2655346676065f844a2ef3df",
                "circleci-checks",
                '{"workflow-id":"c0d92df0-7d09-4774-af5d-6076bc47768e","actor-id":"6f63e7b5-d4fe-41f2-8d06-5627ca3cd61a"}',
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-02-22T14:00:00+00:00"),
                datetime.fromisoformat("2023-02-22T17:00:00+00:00"),
                "b25ab2d8590fc678ced72fe378c0bf2dc04da15c",
                "circleci-checks",
                '{"workflow-id":"71fc25f3-913f-4207-bcc2-c0dc54722932","actor-id":"6a362c69-9e05-474f-b93a-89f145e3851d"}',
            ),
        ]
        deployment_histories = [
            DeploymentHistory(
                "52166f56-7e17-40f5-b7dd-5e8c55d388a8",
                datetime.fromisoformat("2023-02-27T10:15:00+00:00"),
            ),
            DeploymentHistory(
                "71fc25f3-913f-4207-bcc2-c0dc54722932",
                datetime.fromisoformat("2023-02-24T09:30:00+00:00"),
            ),
            DeploymentHistory(
                "b609a9ab-92f2-46b2-b1c2-a9e9b9f3ffc7",
                datetime.fromisoformat("2023-02-23T11:30:00+00:00"),
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

    def test_create_histories_when_a_repository_history_with_no_workflow_id_exists(
        self,
    ):
        repository_histories = [
            RepositoryHistory(
                datetime.fromisoformat("2023-02-25T20:00:00+00:00"),
                datetime.fromisoformat("2023-02-26T22:00:00+00:00"),
                "8eddb4b87a1460b29bce25448623b270465e9715",
            ),
        ]
        deployment_histories = [
            DeploymentHistory(
                "52166f56-7e17-40f5-b7dd-5e8c55d388a8",
                datetime.fromisoformat("2023-02-27T10:15:00+00:00"),
            ),
        ]

        histories = create_histories(repository_histories, deployment_histories)

        assert histories == [
            History(
                datetime.fromisoformat("2023-02-25T20:00:00+00:00"),
                datetime.fromisoformat("2023-02-26T22:00:00+00:00"),
                None,
            ),
        ]
