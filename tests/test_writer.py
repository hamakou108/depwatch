from datetime import datetime
import os
import shutil
from unittest import TestCase
from unittest.mock import patch
from depwatch.writer import write_histories
from depwatch.history import History


class TestWriter(TestCase):
    test_out_dir = "test_out"

    def setUp(self):
        os.mkdir(TestWriter.test_out_dir)

    def test_write_histories(self):
        histories = [
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
        ]

        expected_csv = """first_committed_at,merged_at,deployed_at
2023-02-25T20:00:00+00:00,2023-02-26T22:00:00+00:00,2023-02-27T10:15:00+00:00
2023-02-23T10:05:00+00:00,2023-02-23T11:15:00+00:00,2023-02-23T11:30:00+00:00
2023-02-23T10:00:00+00:00,2023-02-23T11:00:00+00:00,
"""

        with patch.dict("os.environ", {"OUTPUT_DIR": TestWriter.test_out_dir}):
            write_histories("test.csv", histories)

        assert os.path.exists(f"{TestWriter.test_out_dir}/test.csv")

        # CSVファイルの内容を確認
        with open(f"{TestWriter.test_out_dir}/test.csv", "r") as f:
            result_csv = f.read()
            assert result_csv == expected_csv

    def tearDown(self):
        shutil.rmtree(TestWriter.test_out_dir)
