from datetime import date


class DateRange:
    def __init__(
        self,
        start: date | None = None,
        end: date | None = None,
    ):
        self.start = start
        self.end = end

    @staticmethod
    def from_str(string: str):
        try:
            start_date_str, end_date_str = string.split("..")
            start_date = (
                date.fromisoformat(start_date_str) if start_date_str != "" else None
            )
            end_date = date.fromisoformat(end_date_str) if end_date_str != "" else None
            return DateRange(start_date, end_date)
        except ValueError:
            raise ValueError(
                "Invalid date range string format. Expected 'YYYY-MM-DD..YYYY-MM-DD'."
            )

    def __str__(self):
        start_str = self.start if self.start is not None else ""
        end_str = self.end if self.end is not None else ""
        return f"{start_str}..{end_str}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.start, self.end) == (other.start, other.end)

        return False


def convert_date_range_to_str_for_search_query(date_range: DateRange) -> str | None:
    if date_range.start is not None and date_range.end is not None:
        return str(date_range)
    elif date_range.start is not None and date_range.end is None:
        return f">={str(date_range.start)}"
    elif date_range.start is None and date_range.end is not None:
        return f"<={str(date_range.end)}"
    else:
        return None
