import csv
import os

from depwatch.history import History


def write_histories(filename: str, histories: list[History]):
    dirname = str(os.environ.get("OUTPUT_DIR") or "")
    dirname = dirname if dirname != "" else "."

    with open(dirname + "/" + filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(History.keys())
        for h in histories:
            writer.writerow(h.values())
