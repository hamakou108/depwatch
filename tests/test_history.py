from datetime import datetime
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
            [
                {
                    "name": "awesome_workflow",
                    "external_id": '{"workflow-id":"72d1d896-cfbe-48e2-a023-51edb6438b9f","actor-id":"5ead47d7-6407-4264-a150-7f68b8c98631"}',
                    "app": {
                        "slug": "circleci-checks",
                    },
                },
            ],
        )

        assert rh.get_workflow_id() == "72d1d896-cfbe-48e2-a023-51edb6438b9f"

    def test_repository_history_get_workflow_id_when_check_runs_is_empty(
        self,
    ) -> None:
        rh = RepositoryHistory(
            datetime.fromisoformat("2023-04-26T20:00:00+00:00"),
            datetime.fromisoformat("2023-04-26T22:00:00+00:00"),
            "b30000653abd86ff77b2a3e59b427896f4b16ccf",
            [],
        )

        assert rh.get_workflow_id() == None

    def test_repository_history_get_workflow_id_when_the_check_run_app_slug_is_not_supported(
        self,
    ) -> None:
        rh = RepositoryHistory(
            datetime.fromisoformat("2023-04-26T20:00:00+00:00"),
            datetime.fromisoformat("2023-04-26T22:00:00+00:00"),
            "b30000653abd86ff77b2a3e59b427896f4b16ccf",
            [
                {
                    "name": "awesome_workflow",
                    "external_id": '{"foo":"bar"}',
                    "app": {
                        "slug": "custom-checks",
                    },
                },
            ],
        )

        assert rh.get_workflow_id() == None

    def test_repository_history_get_workflow_id_when_workflow_name_is_specified(
        self,
    ) -> None:
        rh = RepositoryHistory(
            datetime.fromisoformat("2023-04-26T20:00:00+00:00"),
            datetime.fromisoformat("2023-04-26T22:00:00+00:00"),
            "b30000653abd86ff77b2a3e59b427896f4b16ccf",
            [
                {
                    "name": "not_target",
                    "external_id": '{"workflow-id":"72d1d896-cfbe-48e2-a023-51edb6438b9f","actor-id":"5ead47d7-6407-4264-a150-7f68b8c98631"}',
                    "app": {
                        "slug": "circleci-checks",
                    },
                },
                {
                    "name": "target",
                    "external_id": '{"workflow-id":"0ba8c279-3f07-40a2-bf86-5df5e60f3c74","actor-id":"d5f1a47d-867a-46c6-8bbc-0b38f908d4f7"}',
                    "app": {
                        "slug": "circleci-checks",
                    },
                },
                {
                    "name": "not_target",
                    "external_id": '{"workflow-id":"c7b22720-23e0-49f8-9b43-47b4cf457a8f","actor-id":"84f7de2f-ca21-4609-83ad-bbc148298b82"}',
                    "app": {
                        "slug": "circleci-checks",
                    },
                },
            ],
        )

        assert rh.get_workflow_id("target") == "0ba8c279-3f07-40a2-bf86-5df5e60f3c74"

    def test_repository_history_get_workflow_id_when_workflow_name_is_specified_but_does_not_exist(
        self,
    ) -> None:
        rh = RepositoryHistory(
            datetime.fromisoformat("2023-04-26T20:00:00+00:00"),
            datetime.fromisoformat("2023-04-26T22:00:00+00:00"),
            "b30000653abd86ff77b2a3e59b427896f4b16ccf",
            [
                {
                    "name": "not_target",
                    "external_id": '{"workflow-id":"72d1d896-cfbe-48e2-a023-51edb6438b9f","actor-id":"5ead47d7-6407-4264-a150-7f68b8c98631"}',
                    "app": {
                        "slug": "circleci-checks",
                    },
                },
            ],
        )

        assert rh.get_workflow_id("target") == None

    def test_convert_repository_history_to_workflow_ids(self) -> None:
        repository_histories = [
            RepositoryHistory(
                datetime.fromisoformat("2023-04-26T20:00:00+00:00"),
                datetime.fromisoformat("2023-04-26T22:00:00+00:00"),
                "b30000653abd86ff77b2a3e59b427896f4b16ccf",
                [
                    {
                        "name": "awesome_workflow",
                        "external_id": '{"workflow-id":"72d1d896-cfbe-48e2-a023-51edb6438b9f","actor-id":"5ead47d7-6407-4264-a150-7f68b8c98631"}',
                        "app": {
                            "slug": "circleci-checks",
                        },
                    },
                ],
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-04-25T20:00:00+00:00"),
                datetime.fromisoformat("2023-04-25T22:00:00+00:00"),
                "cebc0584d4ebeb2da4ed488be5d02c9ca2c7efeb",
                [
                    {
                        "name": "awesome_workflow",
                        "external_id": '{"workflow-id":"da5718a4-d796-4414-a6f7-bb3b26c01bf8","actor-id":"33a61365-e7ef-453c-a105-4aa8d342ca8e"}',
                        "app": {
                            "slug": "circleci-checks",
                        },
                    },
                ],
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-04-24T20:00:00+00:00"),
                datetime.fromisoformat("2023-04-24T22:00:00+00:00"),
                "a6a8e9e33c0854dc742f03e0c48977cad1cec72f",
                [
                    {
                        "name": "awesome_workflow",
                        "external_id": '{"workflow-id":"20219ed8-6bce-4760-9b7c-b50d2eb34099","actor-id":"18b815e9-4438-4fba-b65c-77b224ecc116"}',
                        "app": {
                            "slug": "circleci-checks",
                        },
                    },
                ],
            ),
        ]

        pipeline_list = convert_repository_history_to_workflow_ids(repository_histories)

        assert pipeline_list == [
            "72d1d896-cfbe-48e2-a023-51edb6438b9f",
            "da5718a4-d796-4414-a6f7-bb3b26c01bf8",
            "20219ed8-6bce-4760-9b7c-b50d2eb34099",
        ]

    def test_convert_repository_history_to_workflow_ids_when_workflow_name_is_specified(
        self,
    ) -> None:
        repository_histories = [
            RepositoryHistory(
                datetime.fromisoformat("2023-04-26T20:00:00+00:00"),
                datetime.fromisoformat("2023-04-26T22:00:00+00:00"),
                "b30000653abd86ff77b2a3e59b427896f4b16ccf",
                [
                    {
                        "name": "target",
                        "external_id": '{"workflow-id":"72d1d896-cfbe-48e2-a023-51edb6438b9f","actor-id":"5ead47d7-6407-4264-a150-7f68b8c98631"}',
                        "app": {
                            "slug": "circleci-checks",
                        },
                    },
                    {
                        "name": "not_target",
                        "external_id": '{"workflow-id":"0ba8c279-3f07-40a2-bf86-5df5e60f3c74","actor-id":"d5f1a47d-867a-46c6-8bbc-0b38f908d4f7"}',
                        "app": {
                            "slug": "circleci-checks",
                        },
                    },
                ],
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-04-25T20:00:00+00:00"),
                datetime.fromisoformat("2023-04-25T22:00:00+00:00"),
                "cebc0584d4ebeb2da4ed488be5d02c9ca2c7efeb",
                [
                    {
                        "name": "not_target",
                        "external_id": '{"workflow-id":"da5718a4-d796-4414-a6f7-bb3b26c01bf8","actor-id":"33a61365-e7ef-453c-a105-4aa8d342ca8e"}',
                        "app": {
                            "slug": "circleci-checks",
                        },
                    },
                ],
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-04-24T20:00:00+00:00"),
                datetime.fromisoformat("2023-04-24T22:00:00+00:00"),
                "a6a8e9e33c0854dc742f03e0c48977cad1cec72f",
                [
                    {
                        "name": "not_target",
                        "external_id": '{"workflow-id":"c7b22720-23e0-49f8-9b43-47b4cf457a8f","actor-id":"84f7de2f-ca21-4609-83ad-bbc148298b82"}',
                        "app": {
                            "slug": "circleci-checks",
                        },
                    },
                    {
                        "name": "target",
                        "external_id": '{"workflow-id":"20219ed8-6bce-4760-9b7c-b50d2eb34099","actor-id":"18b815e9-4438-4fba-b65c-77b224ecc116"}',
                        "app": {
                            "slug": "circleci-checks",
                        },
                    },
                ],
            ),
        ]

        pipeline_list = convert_repository_history_to_workflow_ids(
            repository_histories, "target"
        )

        assert pipeline_list == [
            "72d1d896-cfbe-48e2-a023-51edb6438b9f",
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
                [
                    {
                        "name": "awesome_workflow",
                        "external_id": '{"workflow-id":"72d1d896-cfbe-48e2-a023-51edb6438b9f","actor-id":"5ead47d7-6407-4264-a150-7f68b8c98631"}',
                        "app": {
                            "slug": "circleci-checks",
                        },
                    },
                ],
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-04-25T20:00:00+00:00"),
                datetime.fromisoformat("2023-04-25T22:00:00+00:00"),
                "cebc0584d4ebeb2da4ed488be5d02c9ca2c7efeb",
                [],
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-04-24T20:00:00+00:00"),
                datetime.fromisoformat("2023-04-24T22:00:00+00:00"),
                "a6a8e9e33c0854dc742f03e0c48977cad1cec72f",
                [
                    {
                        "name": "awesome_workflow",
                        "external_id": '{"workflow-id":"20219ed8-6bce-4760-9b7c-b50d2eb34099","actor-id":"18b815e9-4438-4fba-b65c-77b224ecc116"}',
                        "app": {
                            "slug": "circleci-checks",
                        },
                    },
                ],
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
                [
                    {
                        "name": "awesome_workflow",
                        "external_id": '{"workflow-id":"52166f56-7e17-40f5-b7dd-5e8c55d388a8","actor-id":"18b815e9-4438-4fba-b65c-77b224ecc116"}',
                        "app": {
                            "slug": "circleci-checks",
                        },
                    },
                ],
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-02-23T10:05:00+00:00"),
                datetime.fromisoformat("2023-02-23T11:15:00+00:00"),
                "12d4c5f2a123b6fb77eccb57be1be3a29438fadb",
                [
                    {
                        "name": "awesome_workflow",
                        "external_id": '{"workflow-id":"b609a9ab-92f2-46b2-b1c2-a9e9b9f3ffc7","actor-id":"58f32647-4d45-4b93-9b57-e9712de5ce08"}',
                        "app": {
                            "slug": "circleci-checks",
                        },
                    },
                ],
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-02-23T10:00:00+00:00"),
                datetime.fromisoformat("2023-02-23T11:00:00+00:00"),
                "cbd1519fd8b7daff2655346676065f844a2ef3df",
                [
                    {
                        "name": "awesome_workflow",
                        "external_id": '{"workflow-id":"c0d92df0-7d09-4774-af5d-6076bc47768e","actor-id":"6f63e7b5-d4fe-41f2-8d06-5627ca3cd61a"}',
                        "app": {
                            "slug": "circleci-checks",
                        },
                    },
                ],
            ),
            RepositoryHistory(
                datetime.fromisoformat("2023-02-22T14:00:00+00:00"),
                datetime.fromisoformat("2023-02-22T17:00:00+00:00"),
                "b25ab2d8590fc678ced72fe378c0bf2dc04da15c",
                [
                    {
                        "name": "awesome_workflow",
                        "external_id": '{"workflow-id":"71fc25f3-913f-4207-bcc2-c0dc54722932","actor-id":"6a362c69-9e05-474f-b93a-89f145e3851d"}',
                        "app": {
                            "slug": "circleci-checks",
                        },
                    },
                ],
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
                [],
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
