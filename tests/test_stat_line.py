from datetime import date

import numpy as np

from extremal_box_score.constants import THREE_STAT, SEVEN_STAT
from extremal_box_score.loaders import stat_lines_from_path
from extremal_box_score.stat_line import INVERSION_CONSTANTS

DATE = date(2020, 10, 19)

stat_lines = stat_lines_from_path('./tests/test_data.csv', DATE, SEVEN_STAT)
for s in stat_lines:
    print(s.vector)

ad_line = stat_lines[0]

def test_display_line():
    assert ad_line.display_line == \
        '                 Anthony Davis | LAL | 2020-10-19 |  33 PTS | 11 TRB |  2 AST |  2 BLK |  1 STL |  57.7% FG% |  1 3PT |  0 TO'

def test_vector():
    assert ad_line.vector == (33, 11, 2, 2, 1, 27, INVERSION_CONSTANTS['turnovers'])

def test_recast():
    assert ad_line.recast(THREE_STAT).vector == (33, 11, 2)

def test_key_value():
    """key_value should return a string including the player slug, date, and a unique index for that date matching the load index"""
    assert stat_lines[12].key_value == 'poolejo01_2020-10-19_12'
