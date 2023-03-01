import csv
import os
from datetime import datetime

from depwatch.history import History


def write_histories(filename: str, histories: list[History]):
    dirname = str(os.environ.get("OUTPUT_DIR") or "")
    dirname = dirname if dirname != "" else "."

    with open(dirname + "/" + filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(History.keys())
        for h in histories:
            formatted_values = []
            for v in h.values():
                if isinstance(v, datetime):
                    formatted_values.append(v.isoformat())
                else:
                    formatted_values.append(v)

            writer.writerow(formatted_values)
