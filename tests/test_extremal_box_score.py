from datetime import date
from random import seed

import numpy as np
import pytest

from extremal_box_score.extremal_box_score import ExtremalBoxScore, StateMark
from extremal_box_score.loaders import stat_lines_from_path
from extremal_box_score.constants import THREE_STAT, FilterMethod, SimplexSelection
from extremal_box_score.filter_config import FILTER_CONFIGS

DATE = date(2020, 10, 19)

stat_lines = stat_lines_from_path('./tests/test_data.csv', DATE, THREE_STAT)

ebs = ExtremalBoxScore(stat_lines, THREE_STAT, FILTER_CONFIGS[THREE_STAT])

random_simplex = np.array([
    [9, 4, 2],
    [9, 2, 2],
    [34, 11, 5],
])

another_simplex = np.array([
    (34, 11, 5),
    (21, 2, 2),
    (10, 4, 6)
])

def test_initial_vector_length():
    assert len(ebs.all_vectors) == 44

def test_initial_state_marks(): 
    assert all([s.mark == StateMark.UNKNOWN for s in ebs.state_map.values()])

def test_initial_state_keys():
    assert all([v in ebs.state_map for v in ebs.all_vectors])

def test_random_simplex():
    seed(0)
    assert np.all(ebs.get_random_simplex() == random_simplex)

def test_simplex_filter():
    assert ebs.simplex_filter(another_simplex) == {
        'filtered': [(6,1,1), (9, 2, 2), (0, 0, 0)]
    }

def test_apply_filter_config():
    seed(0)
    ebs.apply_filter_config({
        'dim': 3,
        'simplex_selection': SimplexSelection.RANDOM,
        'filter_methods': (
            {
                'method': FilterMethod.SIMPLEX
            },
        )
    })

    assert len(ebs.filter_log) == 1

def test_filtered_marks():
    assert ebs.state_map[(0,0,0)].mark == StateMark.DOMINATED

def size_candidate_set():
    assert len(ebs.extremal_candidates) == 43

def test_simplex_filter_again():
    assert ebs.simplex_filter(random_simplex) == None

def test_vertex_dominance_filter():
    assert ebs.vertex_dominance_filter(random_simplex) == {
        'filtered': [
            (33, 11, 2), 
            (32, 11, 4), 
            (21, 2, 2), 
            (15, 11, 4), 
            (20, 3, 2), 
            (20, 9, 3),
            (12, 1, 1),
            (20, 2, 3),
            (12, 1, 2),
            (15, 6, 1),
            (15, 1, 2),
            (12, 7, 1),
            (12, 7, 0),
            (7, 4, 1),
            (6, 4, 1),
            (8, 5, 0),
            (6, 3, 1),
            (6, 5, 0),
            (9, 4, 2),
            (6, 1, 1),
            (9, 2, 2),
            (2, 2, 1),
            (5, 1, 0),
            (5, 6, 0),
            (3, 0, 5),
            (3, 0, 0),
            (8, 2, 0),
            (0, 1, 0),
            (0, 3, 0),
            (2, 2, 0),
            (1, 5, 3),
            (0, 1, 1),
            (1, 0, 2),
            (0, 2, 0),
            (2, 0, 0),
            (8, 5, 4),
            (1, 3, 1)
        ]
    }

def test_dominance_filter_config():
    seed(0)
    ebs.apply_filter_config({
        'dim': 3,
        'simplex_selection': SimplexSelection.RANDOM,
        'filter_methods': (
            {
                'method': FilterMethod.VERTEX_DOMINANCE
            },
        )
    })
    assert len(ebs.extremal_candidates) == 6

def test_dominance_filter_log():
    assert len(ebs.filter_log) == 2
    assert ebs.filter_log[1]['stage'] == {
        'method': FilterMethod.VERTEX_DOMINANCE
    }
    assert len(ebs.filter_log[1]['filtered']) == 37

def test_face_combination_filter():
    ebs = ExtremalBoxScore(stat_lines, THREE_STAT, FILTER_CONFIGS[THREE_STAT])
    assert ebs.random_subset_dominance_filter(random_simplex, 1) == {
        'combination': (pytest.approx(0.2589, 1e-4), pytest.approx(.7411, 1e-4), 0),
        'filtered': [
            (6, 1, 1),
            (9, 2, 2),
            (2, 2, 1),
            (5, 1, 0),
            (3, 0, 0),
            (8, 2, 0),
            (0, 1, 0),
            (2, 2, 0),
            (0, 1, 1),
            (1, 0, 2),
            (0, 0, 0),
            (0, 2, 0),
            (2, 0, 0)
        ]
    }

def test_face_combination_filter_config():
    ebs.apply_filter_config({
        'dim': 3,
        'simplex_selection': SimplexSelection.RANDOM,
        'filter_methods': (
            {
                'method': FilterMethod.RANDOM_SUBSET_DOMINANCE,
                'params': {
                    'num_zero_coordinates': 1
                },
                'repeat': 6
            },
        )
    })

    assert len(ebs.filter_log) == 4

def test_full_filter_log():
    seed(0)
    ebs = ExtremalBoxScore(stat_lines, THREE_STAT, FILTER_CONFIGS[THREE_STAT])
    ebs.iterate(1)

    assert len(ebs.extremal_candidates) == 6

def test_iterate_more():
    seed(0)
    ebs = ExtremalBoxScore(stat_lines, THREE_STAT, FILTER_CONFIGS[THREE_STAT])
    ebs.iterate(10)

    assert len(ebs.extremal_candidates) == 3
    