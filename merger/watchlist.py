"""
Step 11: Lists international swimmers who scored last season. Their swims at foreign clubs
can't be pulled from Swimrankings reports, so check their profiles by hand.
"""

import glob
import os

import pandas as pd

from shared.config import INPUT_FOLDER, PREVIOUS_SEASON_REPORT_FOLDER, EVENT_SCORING_DB_FILENAME, WATCHLIST_FILENAME
from shared.events import LIST_OF_SCORED_RELAY_EVENTS

WATCHLIST_PLACE_CUTOFF = 24

def GenerateWatchlist(current_athlete_ids):
    # Lists international swimmers who placed in the top WATCHLIST_PLACE_CUTOFF last season.
    previous_scoring_filename = os.path.join(PREVIOUS_SEASON_REPORT_FOLDER, EVENT_SCORING_DB_FILENAME)
    if not os.path.exists(previous_scoring_filename):
        print(f"⚠️ {previous_scoring_filename} not found; skipping watchlist")
        return []

    previous_df = pd.read_csv(previous_scoring_filename)
    previous_df = previous_df[~previous_df["Event"].isin(LIST_OF_SCORED_RELAY_EVENTS)]
    previous_df = previous_df[previous_df["Place"] <= WATCHLIST_PLACE_CUTOFF]

    # Nationality comes from the Canada-level reports of both seasons
    athlete_to_nation = {}
    nation_files = (glob.glob(os.path.join(PREVIOUS_SEASON_REPORT_FOLDER, "INPUT", "CAN_*_17-99.xlsx")) +
                    glob.glob(os.path.join(INPUT_FOLDER, "CAN_*_17-99.xlsx")))
    for file_path in nation_files:
        for df in pd.read_excel(file_path, sheet_name=None, header=1).values():
            if "NATION" not in df.columns:
                continue
            for name, birthdate, nation in zip(df["FULLNAME"], df["BIRTHDATE"], df["NATION"]):
                athlete_to_nation[f"{str(name).strip()}_{birthdate}"] = nation

    watchlist = []
    for athlete_id, swims in previous_df.groupby("Athlete ID"):
        nation = athlete_to_nation.get(athlete_id, "?")
        if nation == "CAN":
            continue

        best_swim = swims.sort_values("Place").iloc[0]
        events = ", ".join(f"{e} ({p})" for e, p in zip(swims["Event"], swims["Place"]))
        athlete_name, athlete_birthdate = athlete_id.rsplit("_", 1)
        watchlist.append([
            athlete_name,
            athlete_birthdate.split(" ")[0],
            nation,
            best_swim["Team"],
            "Yes" if athlete_id in current_athlete_ids else "No (graduated, or only swum abroad)",
            events
        ])

    watchlist.sort(key=lambda x: x[0])
    watchlist_df = pd.DataFrame(watchlist, columns=["Name", "Birthdate", "Nation", "Team", "Swum for varsity this season", f"Last season top {WATCHLIST_PLACE_CUTOFF} (Place)"])
    watchlist_df.to_csv(WATCHLIST_FILENAME, index=False, encoding="utf-8")

    print(f"\n👀 Watchlist: {len(watchlist)} international swimmers placed top {WATCHLIST_PLACE_CUTOFF} last season. Check their Swimrankings profiles:")
    for row in watchlist:
        print(f"   {row[0]} ({row[2]}, {row[3]}) born {row[1]}: {row[5]}" + ("" if row[4] == "Yes" else "  [not seen this season]"))
    print(f"Saved to {WATCHLIST_FILENAME}\n")
    return watchlist
