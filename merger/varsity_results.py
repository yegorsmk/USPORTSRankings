"""
Step 1: Reads each team's varsity export (e.g. CAN-DAL_2026_SCM_Men.xlsx) into the Results DB.
"""

import glob
import os

import pandas as pd

from shared.config import (
    INPUT_FOLDER, USPORTS_YEAR, PROGRESS_TRACKER_FILENAME, RESULTS_DB_FILENAME, ATHLETE_IDS_FILENAME,
)
from shared.events import COURSE_SCM, LIST_OF_SCORING_EVENTS_BY_GENDER, SHORT_EVENT_TO_LONG_EVENT
from shared.teams import DICT_OF_CONFERENCES_BY_TEAM, SWIMRANKINGS_CLUB_TO_TEAM
from merger.progress_tracker import save_to_progress_tracker

def GenerateResultsDatabase():
    # Always rebuild from INPUT. Loading the previous OUTPUT file here
    # would append every run's rows onto the last run's rows.
    results_db = []
    athlete_ids = []

    # Loop through all varsity .xlsx files (not the Canada-level ones)
    for file_path in glob.glob(os.path.join(INPUT_FOLDER, f"CAN-*_{USPORTS_YEAR}_SCM_*.xlsx")):
        filename = os.path.basename(file_path)
        # Example: CAN-USHER_2026_SCM_Men.xlsx
        club_code = filename.split("_")[0].replace("CAN-", "")  # e.g., "USHER"
        gender_str = filename.split("_")[-1].replace(".xlsx", "")  # "Men" or "Women"

        if club_code not in SWIMRANKINGS_CLUB_TO_TEAM:
            print(f"Skipping {filename}: unknown club code {club_code}")
            continue

        team_name = SWIMRANKINGS_CLUB_TO_TEAM[club_code]
        conference_name = DICT_OF_CONFERENCES_BY_TEAM[team_name]

        print(f"Processing {filename} → {team_name} ({conference_name})")

        # Read all sheets
        sheet_dict = pd.read_excel(file_path, sheet_name=None, header=1)

        for sheet_name, df in sheet_dict.items():
            # Normalize headers
            df.columns = [str(c).strip() for c in df.columns]

            for _, row in df.iterrows():
                # Skip non-scoring events
                if sheet_name not in SHORT_EVENT_TO_LONG_EVENT.keys():
                    continue

                event_name = SHORT_EVENT_TO_LONG_EVENT[sheet_name]
                if event_name not in LIST_OF_SCORING_EVENTS_BY_GENDER[gender_str]:
                    continue

                # Build athlete record
                athlete_name = str(row["FULLNAME"]).strip()
                club_code = str(row["CLUBCODE"]).strip()
                swimtime = str(row["SWIMTIME_N"]).strip()
                aqua_points = row["PTS_FINA"]
                athlete_birthdate = str(row["BIRTHDATE"])

                # Create synthetic AthleteID
                athlete_id = f"{athlete_name}_{athlete_birthdate}"

                results_db.append([
                    athlete_id,             # AthleteID
                    gender_str,             # Gender
                    event_name,             # Event
                    COURSE_SCM,             # Course
                    club_code,              # Team
                    conference_name,        # Conference
                    athlete_name,           # Name
                    swimtime,               # Time
                    aqua_points             # AQUA
                ])

                athlete_ids.append([athlete_id, team_name])

        save_to_progress_tracker(PROGRESS_TRACKER_FILENAME, team_name)
        print(f"✅ Finished {team_name}\n")

    results_df = pd.DataFrame(results_db, columns=['Athlete ID', 'Gender', 'Event', 'Course', 'Team', 'Conference', 'Name', 'Time', 'AQUA'])
    results_df.to_csv(RESULTS_DB_FILENAME, index=False, encoding="utf-8")
    print("Saved Results DB")

    athlete_ids_df = pd.DataFrame(athlete_ids, columns=['Athlete ID', 'Team'])
    athlete_ids_df.to_csv(ATHLETE_IDS_FILENAME, index=False)
    print("Saved Athlete IDs DB")

    return results_db, athlete_ids

def SaveVarsityResults(results_db, athlete_ids):
    # Step 2: Writes both files again. Note the Athlete IDs header becomes 'Athlete_ID' here.
    results_df = pd.DataFrame(results_db, columns=['Athlete ID', 'Gender', 'Event', 'Course', 'Team', 'Conference', 'Name', 'Time', 'AQUA'])
    results_df.to_csv(RESULTS_DB_FILENAME, index=False, encoding="utf-8")

    athlete_ids_df = pd.DataFrame(athlete_ids, columns=['Athlete_ID', 'Team'])
    athlete_ids_df.to_csv(ATHLETE_IDS_FILENAME, index=False, encoding="utf-8")
    print("Varsity Results Database Created")
