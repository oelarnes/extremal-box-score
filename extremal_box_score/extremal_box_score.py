from enum import Enum
from random import sample

import numpy as np

from extremal_box_score.constants import SimplexSelection, FilterMethod
from extremal_box_score.math import get_face_combination, is_dominated, is_in_origin_simplex

class WriteMode(Enum):
    READONLY='ro'
    WRITE='w'
    OVERWRITE='ow'

class StateMark(Enum):
    EXTREMAL='Extremal'
    UNKNOWN='Unknown'
    DOMINATED='Dominated'

class DominanceSpec:
    def __init__(self, filter_method, simplex_sample, combination=None):
        self.filter_method = filter_method
        self.simplex_sample = simplex_sample
        self.combination = combination

class LineState:
    """records the state of a set of stat_lines with the same vector representation"""
    def __init__(self, stat_lines, mark=None, dominance_spec=None):
        vectors = set([s.vector for s in stat_lines])
        if len(vectors) != 1:
            raise ValueError('invalid stat lines passed to LineState')
        self.vector = list(vectors)[0]
        self.stat_lines = stat_lines
        self.mark = mark if mark is not None else StateMark.UNKNOWN
        self.dominance_spec = dominance_spec
    
    def add(self, stat_line):
        if self.vector != stat_line.vector:
            raise ValueError('invalid stat line added to LineState')

        return LineState(self.stat_lines + [stat_line], self.mark, self.dominance_spec)

    def set_mark(self, mark, dominance_spec=None):
        return LineState(self.stat_lines, mark, dominance_spec if dominance_spec is not None else self.dominance_spec)

class ExtremalBoxScore:
    """
    represents a collection of stat lines in some stage of processing to determine the extremal set according to some param set. 
    Lines are tagged as 'candidate' if they may or may not be extremal, and 'known_extremal' if they are known to be extremal. The 'extremal'
    set is the union of the candidate set and the known extremal set.

    A new ExtremalBoxScore is generated by self.apply(filter_config, )
    """
    def __init__(
        self, 
        stat_lines: list, 
        params:list, 
        filter_config: dict,
    ):
        self.params = params
        self.dim = len(params)
        self.stat_lines = stat_lines
        self.active_filter_config = filter_config
        self.filter_log = []
        self.state_map = self.unmarked_state_map()

    def unmarked_state_map(self):
        state_map = {}
        for s in self.stat_lines:
            if s.vector in state_map:
                state_map[s.vector] = state_map[s.vector].add(s)
            else:
                state_map[s.vector] = LineState([s])
        return state_map

    def get_random_simplex(self):
        """always a number equal to dim(params). If non-singular, defines a hyperplane that forms the outer boundary of
        a dominance set in the first orthant poset."""
        return np.array(sample(self.extremal_candidates, self.dim))

    def simplex_filter(self, simplex_sample):
        candidates = self.filtering_candidates
        filtered = [c for c in candidates if is_in_origin_simplex(simplex_sample, c)]
        if len(filtered):
            return {
                'filtered': filtered
            }

    def vertex_dominance_filter(self, simplex_sample):
        candidates = self.filtering_candidates
        filtered = [c for c in candidates if is_dominated(simplex_sample, np.array(c))]
        if len(filtered):
            return {
                'filtered': filtered
            }

    def random_subset_dominance_filter(self, simplex_sample, num_zero_coordinates):
        candidates = self.filtering_candidates
        combination = get_face_combination(self.dim, num_zero_coordinates)
        face_point = np.matmul(combination, simplex_sample)
        filtered = [c for c in candidates if is_dominated([face_point], np.array(c))]
        if len(filtered):
            return {
                'filtered': filtered,
                'combination': tuple(combination)
            }

    def apply_filter_stage(self, stage, simplex_sample):
        filter_method_map = {
            FilterMethod.SIMPLEX: self.simplex_filter,
            FilterMethod.VERTEX_DOMINANCE: self.vertex_dominance_filter,
            FilterMethod.RANDOM_SUBSET_DOMINANCE: self.random_subset_dominance_filter,
        }

        if stage['method'] not in filter_method_map:
            raise ValueError(f"Invalid filter method {stage['method']}")
        return filter_method_map[stage['method']](simplex_sample, **stage.get('params',{}))

    def apply_filter_config(self, filter_config, index=None):
        simplex_selection_method_map = {
            SimplexSelection.RANDOM: self.get_random_simplex
        }

        if filter_config['dim'] != len(self.params):
            raise ValueError(f"Invalid filter config dimension {filter_config['dim']} for param set {self.params}.")
        if filter_config['simplex_selection'] not in simplex_selection_method_map:
            raise ValueError(f'Invalid simplex selection {filter_config["simplex_selection"]}.')

        sample_simplex = simplex_selection_method_map[filter_config['simplex_selection']]()

        for stage in filter_config['filter_methods']:
            for i in range(stage.get('repeat', 1)):
                results = self.apply_filter_stage(stage, sample_simplex)
                if results is not None:
                    if 'filtered' in results:
                        for f in results['filtered']:
                            self.state_map[f] = self.state_map[f].set_mark(
                                StateMark.DOMINATED, 
                                DominanceSpec(stage['method'], sample_simplex, results.get('combination'))
                            )
                
                    self.filter_log.append({
                        'filter_config': filter_config,
                        'index': index,
                        'stage': stage,
                        'sample_simplex': sample_simplex,
                        'filtered': results.get('filtered'),
                        'extremal': results.get('extremal')
                    })

    def iterate(self, count):
        for i in range(count):
            self.apply_filter_config(self.active_filter_config, i)

    @property
    def all_vectors(self):
        return list(self.state_map.keys())

    @property
    def extremal_candidates(self):
        return [v for v in self.all_vectors if self.state_map[v].mark in (StateMark.EXTREMAL, StateMark.UNKNOWN)]
    
    @property
    def filtering_candidates(self):
        return [v for v in self.all_vectors if self.state_map[v].mark == StateMark.UNKNOWN]
