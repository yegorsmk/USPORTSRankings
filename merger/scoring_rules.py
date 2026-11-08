"""
Points per place, relay multipliers, and how many swims count.
"""

from shared.config import RUN_MODE, RUN_MODE_USPORTS, RUN_MODE_CANADA_WEST, RUN_MODE_MCGILL
from shared.events import COURSE_SCM

## POINTS PER PLACE
USPORTS_POINTS = {
    1 : 32,
    2 : 28,
    3 : 27,
    4 : 26,
    5 : 25,
    6 : 24,
    7 : 23,
    8 : 22,
    9 : 20,
    10 : 17,
    11 : 16,
    12 : 15,
    13 : 14,
    14 : 13,
    15 : 12,
    16 : 11,
    17 : 9,
    18 : 7,
    19 : 6,
    20 : 5,
    21 : 4,
    22 : 3,
    23 : 2,
    24 : 1
}

CANWEST_POINTS = {
    1 : 24,
    2 : 21,
    3 : 20,
    4 : 19,
    5 : 18,
    6 : 17,
    7 : 16,
    8 : 15,
    9 : 14,
    10 : 13,
    11 : 11,
    12 : 10,
    13 : 9,
    14 : 8,
    15 : 7,
    16 : 6,
    17 : 5,
    18 : 4,
    19 : 3,
    20 : 2
}

if RUN_MODE == RUN_MODE_USPORTS:
    PLACE_TO_POINTS = USPORTS_POINTS
elif RUN_MODE == RUN_MODE_CANADA_WEST:
    PLACE_TO_POINTS = CANWEST_POINTS
elif RUN_MODE == RUN_MODE_MCGILL:
    PLACE_TO_POINTS = USPORTS_POINTS

SCORING_COURSES = [COURSE_SCM]

## RELAYS
CANADA_WEST_RELAY_SCORE_MODIFIER = 2
U_SPORTS_RELAY_SCORE_MODIFIER = 1

if RUN_MODE == RUN_MODE_USPORTS:
    RELAY_SCORE_MODIFIER = U_SPORTS_RELAY_SCORE_MODIFIER # 2 for CanWest, 1 for U SPORTS
elif RUN_MODE == RUN_MODE_CANADA_WEST:
    RELAY_SCORE_MODIFIER = CANADA_WEST_RELAY_SCORE_MODIFIER
elif RUN_MODE == RUN_MODE_MCGILL:
    RELAY_SCORE_MODIFIER = U_SPORTS_RELAY_SCORE_MODIFIER

## LIMITS
MAXIMUM_SCORED_SWIMS_PER_SWIMMER = 4

## NOT CURRENTLY USED
RELAY_START_ALLOWANCE = 0.5
SCM_TO_LCM_CONVERSION_FACTOR = 1.03
NUMBER_OF_INDIVIDUAL_EVENTS_TO_SCORE = 4
MAXIMUM_SCORED_RELAYS_PER_TEAM_AND_GENDER = 1

EXEMPT_IDS = []
#EXEMPT_IDS = ["4342739", "5627823", "4786149", "5339517", "4073747"]
#EXEMPT_IDS = ["5492416", "5753229", "4908307", "5394238", "5029821", "5532239", "5192697", "4969912"]  # Foreign kids that don't have Swimrankings Athlete page functionality

DO_NOT_COLLECT_IDS = ["4454358", "4596667", "4570202"]  # Finlay Knox, Blake Tierney, Hugh McNeill

def placeToPoints(p):
    points = 0
    if p in PLACE_TO_POINTS:
        points = PLACE_TO_POINTS[p]
    return points
