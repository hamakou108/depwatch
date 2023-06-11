from unittest.mock import patch, Mock
from depwatch.main import app
from typer.testing import CliRunner


runner = CliRunner()


class TestMain:
    @patch("depwatch.main.generate_histories")
    def test_main(self, mock_generate_histories: Mock):
        result = runner.invoke(app, ["hamakou108/my_project"])

        assert "✨✨ Completed! ✨✨" in result.stdout
        assert result.exit_code == 0
        mock_generate_histories.assert_called_once_with(
            "hamakou108/my_project", False, 100, None
        )

    @patch("depwatch.main.generate_histories")
    def test_main_with_all_args(self, mock_generate_histories: Mock):
        result = runner.invoke(
            app,
            [
                "hamakou108/my_project",
                "--code-only",
                "--limit",
                "10",
                "--workflow-name",
                "deploy",
            ],
        )

        assert result.exit_code == 0
        mock_generate_histories.assert_called_once_with(
            "hamakou108/my_project", True, 10, "deploy"
        )
