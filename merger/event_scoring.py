"""
Steps 3 and 4: Ranks and scores every swim, then keeps each swimmer's top 4 swims and each
team's fastest relay, and ranks and scores those again.

Each step re-reads the previous step's CSV on purpose: that turns every value back into text,
which the sorting in SelectScoredSwims relies on (e.g. x[8].replace(...)).
"""

import csv

from shared.config import COMBINED_RESULTS_DB_FILENAME, EVENT_SCORING_DB_FILENAME, RESTRICTED_EVENT_SCORING_DB_FILENAME
from shared.events import GENDER_MEN, GENDER_WOMEN, LIST_OF_SCORING_EVENTS_BY_GENDER, LIST_OF_SCORED_RELAY_EVENTS
from shared.times import timeToSec
from merger.scoring_rules import SCORING_COURSES, RELAY_SCORE_MODIFIER, MAXIMUM_SCORED_SWIMS_PER_SWIMMER, placeToPoints

def AssignPlacesAndScores(rows):
    """
    Sorts rows by Gender, Event, Course, and Time, then appends Place, Score, and Group to each row.
    Changes rows in place.
    """
    rows.sort(key=lambda x: (x[1], x[2], x[3], float(timeToSec(x[7]))))

    current_group = None
    place = 0

    for row in rows:
        gender = row[1]
        event = row[2]
        course = row[3]

        group = (gender, event, course)
        group_str = gender + "'s " + event + " " + course

        if group != current_group:
            # New group, reset place
            current_group = group
            place = 1
        else:
            place += 1

        # Assign place
        row.append(place)

        # Assign score using placeToPoints
        if event in LIST_OF_SCORING_EVENTS_BY_GENDER[gender] and course in SCORING_COURSES:
            points = placeToPoints(place)

            # Double Points for Relays
            if "x" in event:
                points *= RELAY_SCORE_MODIFIER

            row.append(points)
        else:
            row.append(0)

        row.append(group_str)

def ScoreAllSwims():
    # Step 3a: Rank and score every swim in the Combined Results DB
    with open(COMBINED_RESULTS_DB_FILENAME, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        event_scoring_df = [row for row in reader]

    AssignPlacesAndScores(event_scoring_df)

    with open(EVENT_SCORING_DB_FILENAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Athlete ID", "Gender", "Event", "Course", "Team", "Conference", "Name", "Time", "AQUA", "Place", "Score", "Group"])  # Header
        writer.writerows(event_scoring_df)

def SelectScoredSwims():
    """
    Step 3b: Restrict the event scores by Top 4 Swims per Swimmer and Top 1 Swim per relay.
    """
    # Load Event Scores, which are unrestricted
    with open(EVENT_SCORING_DB_FILENAME, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        event_scoring_df = [row for row in reader]

    individual_athletes = set()
    relay_teams = set()

    for row in event_scoring_df:
        event = row[2]
        name = row[6]
        team = row[4]

        if 'x' not in event:  # Individual event
            individual_athletes.add(name)

        else:  # Relay event
            relay_teams.add(team)

    # Get Top 4 Swims for Each Individual
    # NOTE: grouped by Name, not Athlete ID, so two swimmers with the same name share one limit
    top_individual_swims = []
    for individual_athlete in sorted(individual_athletes):  # sorted: set order changes between runs
        athlete_swims = [row for row in event_scoring_df if row[6] == individual_athlete]

        # Sort by Score (Descending), then AQUA (Descending), then Time (Ascending)
        athlete_swims.sort(key=lambda x: (-float(x[10]), -float(x[8]) if x[8].replace('.', '', 1).isdigit() else 0, float(timeToSec(x[7]))))

        # Select Top 4 Swims
        top_individual_swims.extend(athlete_swims[:MAXIMUM_SCORED_SWIMS_PER_SWIMMER])

    # Get Top 1 Swim for Each Relay
    top_relay_swims = []

    for team in sorted(relay_teams):
        for gender in [GENDER_MEN, GENDER_WOMEN]:
            for relay_event in LIST_OF_SCORED_RELAY_EVENTS:
                # collect all relay swims for (team, gender, relay_event)
                relay_candidates = [
                    row for row in event_scoring_df
                    if row[4] == team and row[1] == gender and row[2] == relay_event
                ]

                if relay_candidates:
                    # sort by time ascending (fastest first)
                    relay_candidates.sort(key=lambda x: float(timeToSec(x[7])))
                    top_relay = relay_candidates[0]
                    top_relay_swims.append(top_relay)

    return top_individual_swims + top_relay_swims

def RescoreSelectedSwims(rescored_df):
    # Step 4: Re-rank and re-score only the swims that count
    AssignPlacesAndScores(rescored_df)

    with open(RESTRICTED_EVENT_SCORING_DB_FILENAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Athlete ID", "Gender", "Event", "Course", "Team", "Conference", "Name", "Time", "AQUA", "Old Place", "Old Score", "Group", "New Place", "New Score"])  # Header
        writer.writerows(rescored_df)
