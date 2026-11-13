"""
Runs every merger step in order. Start here to follow the whole flow.
This file was created on February 24th, 2026 to facilitate the Merge method of U SPORTS rankings.
"""

from merger.varsity_results import GenerateResultsDatabase, SaveVarsityResults
from merger.club_results import GenerateClubResultsDatabase
from merger.combine import MergeVarsityAndClubResults, AddManualResults, RemoveIneligibleAthletes, SaveCombinedResults
from merger.event_scoring import ScoreAllSwims, SelectScoredSwims, RescoreSelectedSwims
from merger.team_scoring import (
    LoadScoredSwims, AggregateTeamScores, SaveTeamRankings,
    AggregateScoresByGroup, BuildTeamBreakdown, SaveTeamBreakdown,
)
from merger.watchlist import GenerateWatchlist

def main():
    ## Step 1: Get a list of U SPORTS swimmers
    results_db, athlete_ids = GenerateResultsDatabase()
    print("Done Step 1/10")

    ## Step 2: Output to CSV Files
    SaveVarsityResults(results_db, athlete_ids)
    print("Done Step 2/10")

    ## Step 2.5 (Dec 16th, 2024 - Jan 25th, 2024): Get Club Results. Not every swimmer always represents their varsity tag,
    ## so we use their Swimrankings ID to get their PBs from this season.
    print("Generating Club Database")
    GenerateClubResultsDatabase()
    print("Club Results Database Generated")
    print("Done Step 2.5/10")

    ## Step 2.75 (Feb 24th, 2026): Merge Club Results with Varsity Results (Varsity Team Tag Enforcement)
    combined_df, varsity_header, athlete_to_varsity_team = MergeVarsityAndClubResults()

    ## Step 2.8 (Nov 6th, 2026): Add manual results (swims at foreign clubs), keeping whichever time is faster
    AddManualResults(combined_df, athlete_to_varsity_team)
    print("Done Step 2.8/10")

    ## Step 2.9 (Nov 10th, 2026): Remove ineligible athletes
    RemoveIneligibleAthletes(combined_df)

    SaveCombinedResults(varsity_header, combined_df)
    print("Done Step 2.9/10")

    ## Step 3: Rank and score every swim, then keep the swims that count
    ScoreAllSwims()
    rescored_df = SelectScoredSwims()
    print("Done Step 3/10")

    ## Step 4: Re-rank and re-score the swims that count
    RescoreSelectedSwims(rescored_df)
    print("Done Step 4/10")

    ## Step 5: Load the re-scored swims
    team_scoring_df = LoadScoredSwims()
    print("Done Step 5/10")

    ## Step 6: Aggregate scores by team
    club_scores, mens_club_scores, womens_club_scores = AggregateTeamScores(team_scoring_df)
    print("Done Step 6/10")

    ## Step 7: Rank the teams
    SaveTeamRankings(club_scores, mens_club_scores, womens_club_scores)
    print("Done Step 7/10")

    ## Steps 8 to 10: Per-event team breakdown
    club_group_scores = AggregateScoresByGroup(team_scoring_df)
    print("Done Step 8/10")

    breakdown_data = BuildTeamBreakdown(club_group_scores)
    print("Done Step 9/10")

    SaveTeamBreakdown(breakdown_data)
    print("Done Step 10/10")

    ## Step 11 (Nov 6th, 2026): Print the watchlist last so it isn't lost in the output above
    GenerateWatchlist(set(athlete_to_varsity_team))
    print("Done!")
