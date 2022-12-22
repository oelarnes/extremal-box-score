from enum import Enum

from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM, TEAM_NAME_TO_TEAM

TEAM_TO_TEAM_NAME = {
    v.name: k for k, v in TEAM_NAME_TO_TEAM.items()
}

TEAM_NAME_TO_ABBREVIATION = {
    TEAM_TO_TEAM_NAME[v.name]: k for k, v in TEAM_ABBREVIATIONS_TO_TEAM.items()
}

class Stats(Enum):
    POINTS = 'points'
    TOTAL_REBOUNDS = 'total_rebounds'
    ASSISTS = 'assists'
    BLOCKS = 'blocks'
    STEALS = 'steals'
    MISSED_FIELD_GOALS = 'missed_field_goals'
    TURNOVERS = 'turnovers'
    MISSED_FREE_THROWS = 'missed_free_throws'
    OFFENSIVE_REBOUNDS = 'offensive_rebounds'
    PERSONAL_FOULS = 'personal_fouls'
    MISSED_POINTS = 'missed_points'

THREE_STAT = (
    Stats.POINTS,
    Stats.TOTAL_REBOUNDS,
    Stats.ASSISTS
)

FIVE_STAT = THREE_STAT + (
    Stats.BLOCKS,
    Stats.STEALS
)

SEVEN_STAT = FIVE_STAT + (
    Stats.MISSED_POINTS,
    Stats.TURNOVERS
)

class SimplexSelection(Enum):
    RANDOM='random'

class FilterMethod(Enum):
    SIMPLEX='simplex'
    VERTEX_DOMINANCE='vertex_dominance'
    RANDOM_SUBSET_DOMINANCE='random_subset_dominance'
