from extremal_box_score.constants import Stats, TEAM_NAME_TO_ABBREVIATION
from extremal_box_score.utils import lpad, format_pct

INVERSION_CONSTANTS = {
    Stats.MISSED_FIELD_GOALS.value: 43,
    Stats.TURNOVERS.value: 15,
    Stats.MISSED_FREE_THROWS.value: 24,
    Stats.PERSONAL_FOULS.value: 6,
    Stats.MISSED_POINTS.value: 110
}

class StatLine:
    """
    A player stat line for one game. Our object of study.
    line = ScoreLine(score_data, date)

    For a paramater, use line.get(param) for a None-defaulted value.
    Use line.get_num(param) for a first-orthant numerical value monotone in superior performance.
    
    """
    def __init__(self, raw_stat_line, date, index, params):
        self.raw_stat_line = raw_stat_line
        self.date = date
        self.index = index # the index of the stat line on the given day's file
        self.key_value = f"{raw_stat_line['slug']}_{date.isoformat()}_{index}"
        self.vector = self.vector_for_params(params)
        self.display_line = self.get_display_line()

    def recast(self, params):
        return StatLine(self.raw_stat_line, self.date, self.index, params)
    
    def get(self, attr):
        return getattr(self, attr, self.raw_stat_line.get(attr, None))
    
    def get_num(self, attr):
        if attr in INVERSION_CONSTANTS:
            return INVERSION_CONSTANTS[attr] - int(self.get(attr) or 0)
        else:
            return int(self.get(attr) or 0)

    @property
    def points(self):
        return 2 * self.get_num('made_field_goals') + self.get_num('made_three_point_field_goals') + self.get_num('made_free_throws')
    
    @property
    def total_rebounds(self):
        return self.get_num('defensive_rebounds') + self.get_num('offensive_rebounds')

    @property
    def missed_free_throws(self):
        if self.get('attempted_free_throws') is None:
            return None
        else:
            return self.get_num('attempted_free_throws') - self.get_num('made_free_throws')

    @property
    def missed_field_goals(self):
        if self.get('attempted_field_goals') is None:
            return None
        else:
            return self.get_num('attempted_field_goals') - self.get_num('made_field_goals')
    
    @property
    def missed_points(self):
        if self.get('missed_field_goals') is None or self.get('missed_free_throws') is None:
            return None
        else:
            return 2 * self.get_num('missed_field_goals') + self.get_num('missed_free_throws')

    @property
    def field_goal_percentage(self):
        if self.get_num('attempted_field_goals') == 0:
            return None

        return self.get_num('made_field_goals') / self.get_num('attempted_field_goals')

    @property
    def team_abbreviation(self):
        return TEAM_NAME_TO_ABBREVIATION.get(self.get('team'))

    def vector_for_params(self, params: list):
        """
        A vector (np.array) in the nonnegative orthant representing the score line. Increasing in each dimension independently represents superior performance 
        """
        return tuple(self.get_num(param.value) for param in params)

    def get_display_line(self):
        return " | ".join([
            lpad(self.get('name'), 30),
            lpad(self.get('team_abbreviation'), 3),
            self.date.isoformat(),
            f"{lpad(self.get('points'), 3)} PTS",
            f"{lpad(self.get('total_rebounds'), 2)} TRB",
            f"{lpad(self.get('assists'), 2)} AST",
            f"{lpad(self.get('blocks'), 2)} BLK",
            f"{lpad(self.get('steals'), 2)} STL",
            f"{format_pct(self.get('field_goal_percentage'))} FG%",
            f"{lpad(self.get('made_three_point_field_goals'), 2)} 3PT",
            f"{lpad(self.get('turnovers'), 2)} TO"
        ])
