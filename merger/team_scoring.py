"""
Steps 5 to 10: Adds up each team's points into the team rankings and the per-event breakdown.
"""

import csv

from shared.config import (
    RESTRICTED_EVENT_SCORING_DB_FILENAME, TEAM_SCORING_DB_FILENAME,
    MENS_TEAM_SCORING_DB_FILENAME, WOMENS_TEAM_SCORING_DB_FILENAME, TEAM_BREAKDOWN_DB_FILENAME,
)
from shared.events import GENDER_MEN, GENDER_WOMEN, LIST_OF_SCORING_EVENTS_BY_GENDER
from shared.teams import DICT_OF_CONFERENCES_BY_TEAM, SWIMRANKINGS_CLUB_TO_TEAM
from merger.scoring_rules import SCORING_COURSES

CLUB_EVENT_TOTAL = "TOTAL"

def LoadScoredSwims():
    # Step 5: Load the restricted (re-scored) swims
    with open(RESTRICTED_EVENT_SCORING_DB_FILENAME, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return [row for row in reader]

def AggregateTeamScores(team_scoring_df):
    """
    Step 6: Aggregate scores by team.
    Only the CLUB_EVENT_TOTAL entries are used afterwards.
    :return: (club_scores, mens_club_scores, womens_club_scores)
    """
    club_scores = {}
    mens_club_scores = {}
    womens_club_scores = {}

    for row in team_scoring_df:
        gender = row[1]
        event = row[2]
        club = row[4]
        conference = row[5]
        score = int(row[13])
        group = row[11]

        if club in club_scores:
            if group in club_scores[club]:
                club_scores[club][group] += score

                if gender == GENDER_MEN:
                    if event in mens_club_scores[club]:
                        mens_club_scores[club][event] += score
                    else:
                        mens_club_scores[club][event] = score
                elif gender == GENDER_WOMEN:
                    if event in womens_club_scores[club]:
                        womens_club_scores[club][event] += score
                    else:
                        womens_club_scores[club][event] = score

            club_scores[club][CLUB_EVENT_TOTAL] += score

            if gender == GENDER_MEN:
                mens_club_scores[club][CLUB_EVENT_TOTAL] += score
            elif gender == GENDER_WOMEN:
                womens_club_scores[club][CLUB_EVENT_TOTAL] += score

        else:
            club_scores[club] = {}
            club_scores[club][group] = score
            club_scores[club][CLUB_EVENT_TOTAL] = score

            mens_club_scores[club] = {}
            womens_club_scores[club] = {}

            mens_club_scores[club][CLUB_EVENT_TOTAL] = 0
            womens_club_scores[club][CLUB_EVENT_TOTAL] = 0

            if gender == GENDER_MEN:
                mens_club_scores[club][event] = score
                mens_club_scores[club][CLUB_EVENT_TOTAL] = score
            elif gender == GENDER_WOMEN:
                womens_club_scores[club][event] = score
                womens_club_scores[club][CLUB_EVENT_TOTAL] = score

    return club_scores, mens_club_scores, womens_club_scores

def SaveTeamRanking(filename, scores_by_club):
    # Rank the clubs by total score and write Rank, Team, Score, Conference
    ranked_clubs = sorted(scores_by_club.items(), key=lambda x: x[1].get(CLUB_EVENT_TOTAL, 0), reverse=True)
    ranked_clubs_with_scores = [(club, scores[CLUB_EVENT_TOTAL]) for club, scores in ranked_clubs]
    ranked_clubs_with_scores_with_ranks = [(i + 1, club, score) for i, (club, score) in enumerate(ranked_clubs_with_scores)]

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(['Rank', 'Team', 'Score', 'Conference'])
        for rank, club, score in ranked_clubs_with_scores_with_ranks:
            writer.writerow([rank, club, score, DICT_OF_CONFERENCES_BY_TEAM[SWIMRANKINGS_CLUB_TO_TEAM[club]]])

def SaveTeamRankings(club_scores, mens_club_scores, womens_club_scores):
    # Step 7: Overall, men's, and women's team rankings
    SaveTeamRanking(TEAM_SCORING_DB_FILENAME, club_scores)
    SaveTeamRanking(MENS_TEAM_SCORING_DB_FILENAME, mens_club_scores)
    SaveTeamRanking(WOMENS_TEAM_SCORING_DB_FILENAME, womens_club_scores)

def AggregateScoresByGroup(team_scoring_df):
    # Step 8: Aggregate scores by club and group (e.g. "Men's 100m Freestyle Short Course (25m)")
    club_group_scores = {}

    for row in team_scoring_df:
        gender = row[1]
        event = row[2]
        course = row[3]
        club = row[4]
        score = int(row[13])
        group = row[11]

        if event in LIST_OF_SCORING_EVENTS_BY_GENDER[gender] and course in SCORING_COURSES:
            if club in club_group_scores:
                if group in club_group_scores[club]:
                    club_group_scores[club][group] += score
                else:
                    club_group_scores[club][group] = score
            else:
                club_group_scores[club] = {group: score}

    return club_group_scores

def BuildTeamBreakdown(club_group_scores):
    # Step 9: One [Team, Category, Score] row per club and group
    breakdown_data = []
    for club, group_scores in club_group_scores.items():
        for group_event, score in group_scores.items():
            breakdown_data.append([club, group_event, score])
    return breakdown_data

def SaveTeamBreakdown(breakdown_data):
    # Step 10
    with open(TEAM_BREAKDOWN_DB_FILENAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(['Team', 'Category', 'Score'])
        writer.writerows(breakdown_data)
