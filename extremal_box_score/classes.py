
class FilterStep:
    """
    specifies how to proceed with filtering the candidate points once a 
    """

class FilterConfig:
    """
    specifies how each step of filtering is performed.

    Attributes
    ----------
    spec_json: str
        json which initialized the FilterConfig

    dim: int
        The number of parameters to which the FilterConfig applies

    simplex_selection: {'random', 'sum_sq_weighted', 'train_weighted', 'from_point'} 
        The first step of each filter is to select #dim points, possibly with repetition
        * 'random' : take #dim random points from the candidate set
        * 'sum_sqr_weighted' : take #dim points from the candidate set weighted by the normalized square sum of the coordinates
        * 'reinforcement_weighted': Hypothetical reinforcement-based method. Uniform without training.
        * 'from_point' : for a random point not tagged 'extremal', take a random set of points waterfalling the following logic
            1. on each dimension, find the set of points from the set of candidate points that exceed on that dimension
            2. if each dimension is non-empty, choose uniformly at random one from each dimension, possibly with repetition
            3. if one dimension is empty, take the set of points which equal on that dimension. For that set, choose a random 
            point for this dimension and recurse the algorithm on the remaining dimensions with only that set as candidates.
            4. if the candidate set is empty on some dimension after this process, tag the point 'extremal'
    
    filter_methods: list of FilterStep objects
    """
    def __init__(self, spec_json: str):
        self.spec_json = spec_json

