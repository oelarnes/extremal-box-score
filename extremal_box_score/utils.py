import numpy as np

def incomplete_partition(dim, divisions):
    if divisions == 0:
        return [[0 for d in range(dim)]]
    if dim == 1:
        return [[i] for i in range(divisions + 1)]
    matrix = [[[i] + mat for mat in incomplete_partition(dim-1, divisions - i)] for i in range(divisions + 1)]
    return [item for sublist in matrix for item in sublist]

def complete_partition(dim, divisions):
    incomplete = incomplete_partition(dim-1, divisions)
    return [row + [divisions-sum(row)] for row in incomplete]

def get_simplex_face_grid(dim, score_array):
    divisions = np.max(np.max(score_array, 0) - np.min(score_array, 0))
    division_matrix = complete_partition(dim, divisions)
    return np.matmul(division_matrix, score_array)/divisions

def lpad(input, size):
    text = '' if input is None else str(input)
    return ' ' * (size - len(text)) + text if len(text) < size else text

def format_pct(pct):
    return lpad('N/A', 6) if pct is None else lpad('{:.1f}%'.format(pct * 100), 6)
