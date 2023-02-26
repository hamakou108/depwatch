import csv
import os

from deploywatch.history import History


def write_histories(filename: str, histories: list[History]):
    dirname = os.environ.get('OUTPUT_DIR') if os.environ.get('OUTPUT_DIR', '') != '' else '.'

    with open(dirname + '/' + filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(History.keys())
        for h in histories:
            writer.writerow(h.values())
