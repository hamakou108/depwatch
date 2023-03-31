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
        mock_Github.return_value.get_repo.return_value = (
            self.create_mock_repo_with_pulls()
        )

        result = repository.get_repository_history("hamakou108/my_project", "main", 100)

        assert len(result) == 2
        assert result[0].first_committed_at == datetime(2021, 1, 1, tzinfo=timezone.utc)
        assert result[0].merged_at == datetime(2021, 1, 3, tzinfo=timezone.utc)
        assert len(result[0].merge_commit_sha) == 40

    def create_mock_repo_with_branches(self, branches: list[str]):
        mock_repo = MagicMock()

        mock_branches = []
        for b in branches:
            mock_branch = MagicMock(spec=["name"])
            mock_branch.name = b
            mock_branches.append(mock_branch)

        mock_repo.get_branches.return_value = mock_branches

        return mock_repo

    def create_mock_repo_with_pulls(self):
        mock_repo = MagicMock()

        mock_repo.get_pulls.return_value = [
            self.create_mock_pull(True),
            self.create_mock_pull(False),
            self.create_mock_pull(True),
        ]

        return mock_repo

    def create_mock_pull(self, is_merged: bool):
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
