from time import time
from random import sample, random, shuffle

import numpy as np
from scipy.linalg import solve, det

def is_in_origin_simplex(score_array, v):
    eps = 1e-8
    if det(score_array) != 0:
        solution = solve(score_array.T, v)
        return np.all(np.logical_and(solution < 1 - eps, solution >= 0)) and sum(solution) < 1 - eps
    else:
        return False

def get_face_combination(dim,  zeroes):
    random_data = [0] + sorted([random() for i in range(dim-1-zeroes)]) + [1]
    intervals = [random_data[i+1] - val for i, val in enumerate(random_data[:-1])] + [0 for i in range(zeroes)]
    shuffle(intervals)
    return intervals

def is_dominated(score_array, v):
    if np.any(np.logical_and(np.all(score_array >= v, 1), np.any(score_array > v, 1))):
        return True
