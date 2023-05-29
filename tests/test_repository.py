from datetime import datetime, timezone
import secrets
from unittest.mock import patch, Mock, MagicMock
from depwatch import repository
from depwatch.exception import DepwatchException


class TestRepository:
    @patch("depwatch.repository.Github")
    def test_get_main_branch_with_main_branch(self, mock_Github: Mock):
        mock_Github.return_value.get_repo.return_value = (
            self.create_mock_repo_with_branches(["main"])
        )

        assert repository.get_main_branch("hamakou108/my_project") == "main"

    @patch("depwatch.repository.Github")
    def test_get_main_branch_with_master_branch(self, mock_Github: Mock):
        mock_Github.return_value.get_repo.return_value = (
            self.create_mock_repo_with_branches(["master"])
        )

        assert repository.get_main_branch("hamakou108/my_project") == "master"

    @patch("depwatch.repository.Github")
    def test_get_main_branch_with_other_branch(self, mock_Github: Mock):
        mock_Github.return_value.get_repo.return_value = (
            self.create_mock_repo_with_branches(["foo"])
        )

        try:
            repository.get_main_branch("hamakou108/my_project")
            assert False
        except DepwatchException as e:
            assert str(e) == "'main' or 'master' branch was not found"

    @patch("depwatch.repository.Github")
    def test_get_repository_history(self, mock_Github: Mock):
        mock_repo = MagicMock()
        mock_repo.get_pulls.return_value = [
            self.create_mock_pull(),
            self.create_mock_pull(),
            self.create_mock_pull(),
        ]
        mock_repo.get_commit.return_value = self.create_mock_commit()
        mock_Github.return_value.get_repo.return_value = mock_repo

        result = repository.get_repository_history("hamakou108/my_project", "main", 100)

        assert len(result) == 3
        assert result[0].first_committed_at == datetime(2021, 1, 1, tzinfo=timezone.utc)
        assert result[0].merged_at == datetime(2021, 1, 3, tzinfo=timezone.utc)
        assert len(result[0].merge_commit_sha) == 40
        assert result[0].check_run_app_slug == "circleci-checks"
        assert (
            result[0].check_run_external_id
            == '{"workflow-id":"10d1e2e1-cd4d-4662-a654-ff0cb02ad58d","actor-id":"20a538b5-8416-4419-b8da-a504c3835c4a"}'
        )

    @patch("depwatch.repository.Github")
    def test_get_repository_history_if_a_pull_request_with_no_merge_commit_is_included(
        self, mock_Github: Mock
    ):
        mock_repo = MagicMock()
        mock_repo.get_pulls.return_value = [
            self.create_mock_pull(False),
        ]
        mock_Github.return_value.get_repo.return_value = mock_repo

        result = repository.get_repository_history("hamakou108/my_project", "main", 100)

        assert len(result) == 0

    @patch("depwatch.repository.Github")
    def test_get_repository_history_if_a_merge_commit_with_no_check_runs_is_included(
        self, mock_Github: Mock
    ):
        mock_repo = MagicMock()
        mock_repo.get_pulls.return_value = [
            self.create_mock_pull(),
        ]
        mock_repo.get_commit.return_value = self.create_mock_commit(False)
        mock_Github.return_value.get_repo.return_value = mock_repo

        result = repository.get_repository_history("hamakou108/my_project", "main", 100)

        assert len(result) == 1
        assert result[0].check_run_app_slug == None
        assert result[0].check_run_external_id == None

    def create_mock_repo_with_branches(self, branches: list[str]):
        mock_repo = MagicMock()

        mock_branches = []
        for b in branches:
            mock_branch = MagicMock(spec=["name"])
            mock_branch.name = b
            mock_branches.append(mock_branch)

        mock_repo.get_branches.return_value = mock_branches

        return mock_repo

    def create_mock_commit(self, has_check_runs: bool = True):
        mock_check_run = MagicMock(spec=["app", "external_id"])
        mock_check_run.app.slug = "circleci-checks"
        mock_check_run.external_id = '{"workflow-id":"10d1e2e1-cd4d-4662-a654-ff0cb02ad58d","actor-id":"20a538b5-8416-4419-b8da-a504c3835c4a"}'

        # Unable to import PaginatestList, create mock with required I/F
        check_runs = [mock_check_run] if has_check_runs else []
        mock_check_runs = MagicMock()
        mock_check_runs.__getitem__.side_effect = check_runs.__getitem__
        mock_check_runs.totalCount = len(check_runs)

        mock_commit = MagicMock(spec=["get_check_runs"])
        mock_commit.get_check_runs.return_value = mock_check_runs

        return mock_commit

    def create_mock_pull(self, is_merged: bool = True):
        mock_pull = MagicMock(spec=["get_commits", "merged_at", "merge_commit_sha"])
        mock_commits = []
        for i in range(3):
            mock_commit = MagicMock(spec=["commit"])
            mock_commit.commit.author.date = datetime(
                2021, 1, i + 1, tzinfo=timezone.utc
            )
            mock_commits.append(mock_commit)
        mock_pull.get_commits.return_value = mock_commits
        mock_pull.merged_at = (
            datetime(2021, 1, 3, tzinfo=timezone.utc) if is_merged else None
        )
        mock_pull.merge_commit_sha = secrets.token_hex(20) if is_merged else None

        return mock_pull
