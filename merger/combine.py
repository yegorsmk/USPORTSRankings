"""
Steps 2.75 and 2.8: Merges varsity, club, and manual swims into the Combined Results DB,
keeping each athlete's fastest time per event under their varsity team.
"""

import csv

from shared.config import RESULTS_DB_FILENAME, CLUB_RESULTS_DB_FILENAME, COMBINED_RESULTS_DB_FILENAME, INELIGIBLE_SWIMMERS_IDS
from shared.times import timeToSec
from merger.manual_results import LoadManualResults

def to_sec_safe(t):
    try:
        return timeToSec(t)
    except:
        return float("inf")

def MergeVarsityAndClubResults():
    """
    Step 2.75 (Feb 24th, 2026): Merge Club Results with Varsity Results (Varsity Team Tag Enforcement).
    :return: (combined rows, varsity CSV header, dict of Athlete ID → varsity team code)
    """
    # Load varsity results
    with open(RESULTS_DB_FILENAME, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        varsity_header = next(reader)
        varsity_df = [row for row in reader]

    # Load club results
    with open(CLUB_RESULTS_DB_FILENAME, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        club_header = next(reader)
        club_df = [row for row in reader]

    # Create lookup dictionaries
    # key = (AthleteID, Gender, Event, Course)
    varsity_results = {(r[0], r[1], r[2], r[3]): r for r in varsity_df}
    club_results = {(r[0], r[1], r[2], r[3]): r for r in club_df}

    # Map AthleteID → Varsity (Team, Conference)
    athlete_to_varsity_team = {r[0]: r[4] for r in varsity_df}
    athlete_to_varsity_conf = {r[0]: r[5] for r in varsity_df}

    combined_df = []

    for key, varsity_row in varsity_results.items():
        athlete_id, gender, event, course = key
        varsity_time = varsity_row[7]
        varsity_team = varsity_row[4]
        varsity_conf = varsity_row[5]

        # if also exists in club
        if key in club_results:
            club_row = club_results[key]
            club_time = club_row[7]

            # compare times numerically (convert mm:ss.hh)
            if to_sec_safe(club_time) < to_sec_safe(varsity_time):
                # use faster club row but enforce varsity identity
                updated_row = club_row.copy()
                updated_row[4] = varsity_team
                updated_row[5] = varsity_conf
                combined_df.append(updated_row)
            else:
                combined_df.append(varsity_row)
        else:
            combined_df.append(varsity_row)

    # Add club-only events that belong to known varsity swimmers
    for key, club_row in club_results.items():
        if key not in varsity_results:
            athlete_id = club_row[0]
            if athlete_id in athlete_to_varsity_team:
                # enforce varsity identity for these too
                club_row[4] = athlete_to_varsity_team[athlete_id]
                club_row[5] = athlete_to_varsity_conf[athlete_id]
                combined_df.append(club_row)

    return combined_df, varsity_header, athlete_to_varsity_team

def AddManualResults(combined_df, athlete_to_varsity_team):
    # Step 2.8 (Nov 6th, 2026): Add manual results (swims at foreign clubs), keeping whichever time is faster.
    # Changes combined_df in place.
    combined_index = {(r[0], r[1], r[2], r[3]): i for i, r in enumerate(combined_df)}
    for manual_row in LoadManualResults(athlete_to_varsity_team):
        key = (manual_row[0], manual_row[1], manual_row[2], manual_row[3])
        if key not in combined_index:
            combined_index[key] = len(combined_df)
            combined_df.append(manual_row)
        elif timeToSec(manual_row[7]) < timeToSec(combined_df[combined_index[key]][7]):
            combined_df[combined_index[key]] = manual_row

def SaveCombinedResults(varsity_header, combined_df):
    with open(COMBINED_RESULTS_DB_FILENAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(varsity_header)
        writer.writerows(combined_df)

    print(f"💾 Combined Results DB saved to {COMBINED_RESULTS_DB_FILENAME} ({len(combined_df)} rows)")

def RemoveIneligibleAthletes(combined_df):
    removed = [r for r in combined_df if r[0] in INELIGIBLE_SWIMMERS_IDS]
    combined_df[:] = [r for r in combined_df if r[0] not in INELIGIBLE_SWIMMERS_IDS]
    for athlete_id in sorted({r[0] for r in removed}):
        print(f"🚫 Removed {athlete_id} (ineligible)")
    print(f"Removed {len(removed)} swims by ineligible athletes")