"""
Step 2.5: Reads the Canada-level exports (e.g. CAN_2026_SCM_Men_17-99.xlsx) and keeps
the swims of known varsity athletes, so swims under a club tag still count.
"""

import csv
import glob
import os

import pandas as pd

from shared.config import (
    INPUT_FOLDER, USPORTS_YEAR, ATHLETE_IDS_FILENAME, CLUB_RESULTS_DB_FILENAME, CLUB_ATHLETE_IDS_FILENAME,
)
from shared.events import COURSE_SCM, LIST_OF_SCORING_EVENTS_BY_GENDER, SHORT_EVENT_TO_LONG_EVENT
from shared.teams import DICT_OF_CONFERENCES_BY_TEAM, SWIMRANKINGS_CLUB_TO_TEAM
from shared.times import timeToSec

def GenerateClubResultsDatabase():
    # Load existing varsity athlete IDs (to filter club results)
    varsity_ids = set()
    try:
        with open(ATHLETE_IDS_FILENAME, "r") as file:
            reader = csv.reader(file)
            next(reader)
            varsity_ids = {row[0].strip() for row in reader if row}
            print(f"Loaded {len(varsity_ids)} Varsity Athlete IDs")
    except FileNotFoundError:
        print("⚠️ Varsity Athlete IDs file not found; cannot filter club database.")
        varsity_ids = set()

    # Identify files like CAN_2026_SCM_Men_17-99.xlsx
    canadian_files = glob.glob(os.path.join(INPUT_FOLDER, f"CAN_{USPORTS_YEAR}_SCM_*_17-99.xlsx"))
    if not canadian_files:
        print("⚠️ No Canada-level club files found in INPUT/")
        return []

    club_results_db = []

    for file_path in canadian_files:
        filename = os.path.basename(file_path)
        print(f"📘 Processing Canada-level file: {filename}")

        gender_str = "Men" if "Men" in filename else "Women"

        # Read all event sheets
        sheet_dict = pd.read_excel(file_path, sheet_name=None, header=1)

        for sheet_name, df in sheet_dict.items():
            # Normalize sheet name → Long event name
            if sheet_name not in SHORT_EVENT_TO_LONG_EVENT:
                continue
            event_name = SHORT_EVENT_TO_LONG_EVENT[sheet_name]

            # Skip non-scoring events
            if event_name not in LIST_OF_SCORING_EVENTS_BY_GENDER[gender_str]:
                continue

            # Normalize headers
            df.columns = [str(c).strip().upper() for c in df.columns]

            # Expected columns
            possible_name_cols = ["FULLNAME", "NAME"]
            possible_birth_cols = ["BIRTHDATE", "DOB"]
            possible_time_cols = ["SWIMTIME_N", "SWIMTIME", "TIME"]
            possible_aqua_cols = ["PTS_FINA", "AQUA POINTS"]
            possible_team_cols = ["CLUBCODE", "TEAM"]

            def find_col(possible_cols):
                for col in possible_cols:
                    if col in df.columns:
                        return col
                return None

            name_col = find_col(possible_name_cols)
            birth_col = find_col(possible_birth_cols)
            time_col = find_col(possible_time_cols)
            aqua_col = find_col(possible_aqua_cols)
            team_col = find_col(possible_team_cols)

            if not all([name_col, birth_col, time_col, aqua_col, team_col]):
                print(f"⚠️ Missing key columns in {filename}:{sheet_name}")
                continue

            # Iterate through each swim
            for _, row in df.iterrows():
                athlete_name = str(row[name_col]).strip()
                athlete_birthdate = str(row[birth_col]).strip()
                if not athlete_name or not athlete_birthdate:
                    continue

                athlete_id = f"{athlete_name}_{athlete_birthdate}"
                if athlete_id not in varsity_ids:
                    continue  # only keep if swimmer exists in varsity DB

                swimtime = str(row[time_col]).strip()
                if not swimtime:
                    continue

                aqua_points = row[aqua_col] if pd.notna(row[aqua_col]) else 0
                club_code = str(row[team_col]).strip()

                # Resolve to U SPORTS team if applicable
                if club_code in SWIMRANKINGS_CLUB_TO_TEAM:
                    team_name = SWIMRANKINGS_CLUB_TO_TEAM[club_code]
                    conference_name = DICT_OF_CONFERENCES_BY_TEAM.get(team_name)
                else:
                    team_name = club_code
                    conference_name = "Club"

                # Append record
                club_results_db.append([
                    athlete_id,
                    gender_str,
                    event_name,
                    COURSE_SCM,
                    club_code,
                    conference_name,
                    athlete_name,
                    swimtime,
                    aqua_points
                ])

        print(f"✅ Finished processing {filename}")

    # Deduplicate by (AthleteID, Event, Gender) keeping fastest swimtime
    def time_to_sec_safe(t):
        try:
            return timeToSec(str(t))
        except Exception:
            return float('inf')

    club_df = pd.DataFrame(club_results_db, columns=[
        "Athlete ID", "Gender", "Event", "Course",
        "Team", "Conference", "Name", "Time", "AQUA"
    ])

    if not club_df.empty:
        club_df["TimeSec"] = club_df["Time"].apply(time_to_sec_safe)
        club_df = club_df.sort_values(["Athlete ID", "Event", "Gender", "TimeSec"])
        club_df = club_df.drop_duplicates(subset=["Athlete ID", "Event", "Gender"], keep="first")
        club_df = club_df.drop(columns=["TimeSec"])
    else:
        print("⚠️ No matching club results found for varsity swimmers.")
        return []

    # Save filtered Club Results DB
    club_df.to_csv(CLUB_RESULTS_DB_FILENAME, index=False, encoding="utf-8")
    print(f"💾 Saved filtered Club Results DB ({len(club_df)} rows)")

    # Save matching Club Athlete IDs
    club_ids_df = club_df[["Athlete ID"]].drop_duplicates()
    club_ids_df.to_csv(CLUB_ATHLETE_IDS_FILENAME, index=False, encoding="utf-8")
    print(f"💾 Saved matching Club Athlete IDs ({len(club_ids_df)} athletes)")

    return club_df.values.tolist()
