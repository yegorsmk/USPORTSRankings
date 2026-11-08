"""
Reads swims typed into INPUT/manual_results.xlsx (swims at foreign clubs that Swimrankings reports miss).
"""

import os

import pandas as pd

from shared.config import MANUAL_RESULTS_FILENAME, MANUAL_RESULTS_SHEET
from shared.events import COURSE_SCM, GENDERS, LIST_OF_SCORING_EVENTS_BY_GENDER
from shared.teams import DICT_OF_CONFERENCES_BY_TEAM, SWIMRANKINGS_CLUB_TO_TEAM
from shared.times import timeToSec

def LoadManualResults(athlete_to_varsity_team):
    # Reads swims typed into MANUAL_RESULTS_FILENAME and returns them as Combined Results rows
    if not os.path.exists(MANUAL_RESULTS_FILENAME):
        print("No manual results file found; skipping")
        return []

    df = pd.read_excel(MANUAL_RESULTS_FILENAME, sheet_name=MANUAL_RESULTS_SHEET, dtype={"Time": str})
    df = df.dropna(how="all")

    manual_rows = []
    for index, row in df.iterrows():
        excel_row = index + 2  # +1 for the header, +1 because Excel counts from 1
        athlete_name = str(row["Name"]).strip()
        gender = str(row["Gender"]).strip()
        event_name = str(row["Event"]).strip()

        try:
            # Match the Athlete ID format built from the Swimrankings reports
            athlete_birthdate = str(pd.to_datetime(row["Birthdate"]))
            swimtime = timeToSec(str(row["Time"]).strip())
        except Exception:
            print(f"⚠️ Manual results row {excel_row}: unreadable Birthdate or Time; skipping")
            continue

        if gender not in GENDERS or event_name not in LIST_OF_SCORING_EVENTS_BY_GENDER[gender]:
            print(f"⚠️ Manual results row {excel_row}: unknown Gender/Event '{gender} {event_name}'; skipping")
            continue

        athlete_id = f"{athlete_name}_{athlete_birthdate}"

        # Prefer the team they swim for this season, fall back to the Team column
        if athlete_id in athlete_to_varsity_team:
            club_code = athlete_to_varsity_team[athlete_id]
        else:
            club_code = str(row["Team"]).strip()
            print(f"ℹ️ Manual results row {excel_row}: {athlete_name} has no varsity swims yet, using Team '{club_code}'")

        if club_code not in SWIMRANKINGS_CLUB_TO_TEAM:
            print(f"⚠️ Manual results row {excel_row}: unknown Team '{club_code}'; skipping")
            continue

        conference_name = DICT_OF_CONFERENCES_BY_TEAM[SWIMRANKINGS_CLUB_TO_TEAM[club_code]]
        aqua_points = int(row["AQUA"]) if pd.notna(row["AQUA"]) else 0

        manual_rows.append([
            athlete_id,
            gender,
            event_name,
            COURSE_SCM,
            club_code,
            conference_name,
            athlete_name,
            str(swimtime),  # Seconds, like SWIMTIME_N in the reports
            aqua_points
        ])

    print(f"Loaded {len(manual_rows)} manual results")
    return manual_rows
