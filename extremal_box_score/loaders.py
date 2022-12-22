import csv
import re
from datetime import date

from extremal_box_score.stat_line import StatLine

def stat_lines_from_dated_paths(paths):
    stat_lines = []
    for path in paths:
        date = parse_date_from_path(path)
        stat_lines.append(stat_lines_from_path(path, date))

def stat_lines_from_path(path, date, params):
    with open(path) as csvfile:
        raw_lines = csv.DictReader(csvfile)
        return [StatLine(raw_line, date, i, params) for i, raw_line in enumerate(raw_lines)]

def parse_date_from_path(path):
    match = re.search('/([0-9-]{10})\.', path)
    if match is None:
        raise ValueError(f'path {path} cannot be parsed for date')
    return date.fromisoformat(match.group(1))
