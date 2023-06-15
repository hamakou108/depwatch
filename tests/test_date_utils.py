from datetime import date
from depwatch.date_utils import DateRange, convert_date_range_to_str_for_search_query


class TestDateUtils:
    def test_date_range_from_str(self):
        datasets = [
            "2023-01-01..2023-03-31",
            "2023-01-01..",
            "..2023-03-31",
        ]

        for string in datasets:
            date_range = DateRange.from_str(string)

            assert str(date_range) == string

    def test_date_range_from_str_when_invalid_string_is_provided(self):
        try:
            DateRange.from_str("2023-01-01")
            assert False
        except ValueError as e:
            assert (
                str(e)
                == "Invalid date range string format. Expected 'YYYY-MM-DD..YYYY-MM-DD'."
            )

    def test_date_convert_date_range_to_str_for_search_query(self):
        datasets = [
            [
                date.fromisoformat("2023-01-01"),
                date.fromisoformat("2023-03-31"),
                "2023-01-01..2023-03-31",
            ],
            [date.fromisoformat("2023-01-01"), None, ">=2023-01-01"],
            [None, date.fromisoformat("2023-03-31"), "<=2023-03-31"],
            [None, None, None],
        ]

        for start, end, string in datasets:
            date_range = DateRange(start, end)

            assert convert_date_range_to_str_for_search_query(date_range) == string
