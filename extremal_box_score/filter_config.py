from extremal_box_score.constants import *


FILTER_CONFIGS = {
    THREE_STAT: {
        'dim': 3,
        'simplex_selection': SimplexSelection.RANDOM,
        'filter_methods': (
            {
                'method': FilterMethod.SIMPLEX
            },
            {
                'method': FilterMethod.VERTEX_DOMINANCE
            },
            {
                'method': FilterMethod.RANDOM_SUBSET_DOMINANCE,
                'params': {
                    'num_zero_coordinates': 0
                },
                'repeat': 6
            },
            {
                'method': FilterMethod.RANDOM_SUBSET_DOMINANCE,
                'params': {
                    'num_zero_coordinates': 1
                },
                'repeat': 6
            }
        )
    },
    FIVE_STAT: {
        'dim': 5,
        'simplex_selection': SimplexSelection.RANDOM,
        'filter_methods': (
            {
                'method': FilterMethod.SIMPLEX
            },
            {
                'method': FilterMethod.VERTEX_DOMINANCE
            },
            {
                'method': FilterMethod.RANDOM_SUBSET_DOMINANCE,
                'params': {
                    'num_zero_coordinates': 0,
                },
                'repeat': 10
            },
            {
                'method': FilterMethod.RANDOM_SUBSET_DOMINANCE,
                'params': {
                    'num_zero_coordinates': 1,
                },
                'repeat': 10
            },
            {
                'method': FilterMethod.RANDOM_SUBSET_DOMINANCE,
                'params': {
                    'num_zero_coordinates': 2,
                },
                'repeat': 10
            },
            {
                'method': FilterMethod.RANDOM_SUBSET_DOMINANCE,
                'params': {
                    'num_zero_coordinates': 3,
                 },
                'repeat': 10
            }
        )
    },
    SEVEN_STAT: {
        'dim': 5,
        'simplex_selection': SimplexSelection.RANDOM,
        'filter_methods': (
            {
                'method': FilterMethod.SIMPLEX
            },
            {
                'method': FilterMethod.VERTEX_DOMINANCE
            },
            {
                'method': FilterMethod.RANDOM_SUBSET_DOMINANCE,
                'params': {
                    'num_zero_coordinates': 1,
                },
                'repeat': 14
            },
            {
                'method': FilterMethod.RANDOM_SUBSET_DOMINANCE,
                'params': {
                    'num_zero_coordinates': 1,
                },
                'repeat': 14
            },
            {
                'method': FilterMethod.RANDOM_SUBSET_DOMINANCE,
                'params': {
                    'num_zero_coordinates': 1,
                },
                'repeat': 14
            },
            {
                'method': FilterMethod.RANDOM_SUBSET_DOMINANCE,
                'params': {
                    'num_zero_coordinates': 1,
                },
                'repeat': 14
            },
            {
                'method': FilterMethod.RANDOM_SUBSET_DOMINANCE,
                'params': {
                    'num_zero_coordinates': 1,
                },
                'repeat': 14
            },
            {
                'method': FilterMethod.RANDOM_SUBSET_DOMINANCE,
                'params': {
                    'num_zero_coordinates': 1,
                },
                'repeat': 14
            }
        )
    }
}
