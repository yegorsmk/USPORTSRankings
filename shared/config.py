"""
Run mode, season, and file locations.
"""

## RUN MODE
RUN_MODE_CANADA_WEST = "Canada West"
RUN_MODE_USPORTS = "U SPORTS"
RUN_MODE_MCGILL = "McGill"
RUN_MODE = RUN_MODE_USPORTS

## SEASON
# Year in the Swimrankings export filenames, e.g. CAN-DAL_2026_SCM_Men.xlsx
USPORTS_YEAR = "2026"

## INPUT FILES
INPUT_FOLDER = "./INPUT/"

# Nov 6th, 2026: Swims at foreign clubs aren't in the Canada-level report, so they are typed in by hand
MANUAL_RESULTS_FILENAME = INPUT_FOLDER + "manual_results.xlsx"
MANUAL_RESULTS_SHEET = "Results"

# Nov 6th, 2026: International swimmers who scored last season, worth checking on Swimrankings by hand
PREVIOUS_SEASON_REPORT_FOLDER = "./Archive/2025-2026 Season/March 3rd Report/"

## OUTPUT FILES
OUTPUT_PREFIX = "OUTPUT_"

PROGRESS_TRACKER_FILENAME = OUTPUT_PREFIX + "progress_tracker.txt"
CLUB_PROGRESS_TRACKER_FILENAME = OUTPUT_PREFIX + "club_progress_tracker.txt"   # Not currently used

RESULTS_DB_FILENAME = OUTPUT_PREFIX + "results_db.csv"
ATHLETE_IDS_FILENAME = OUTPUT_PREFIX + "athlete_ids.csv"

CLUB_RESULTS_DB_FILENAME = OUTPUT_PREFIX + "club_results_db.csv"
CLUB_ATHLETE_IDS_FILENAME = OUTPUT_PREFIX + "club_athlete_ids.csv"

COMBINED_RESULTS_DB_FILENAME = OUTPUT_PREFIX + "combined_results_db.csv"

# Read by the website
EVENT_SCORING_DB_FILENAME = OUTPUT_PREFIX + "event_scoring_db.csv"
RESTRICTED_EVENT_SCORING_DB_FILENAME = OUTPUT_PREFIX + "restricted_event_scoring_db.csv"

TEAM_SCORING_DB_FILENAME = OUTPUT_PREFIX + "team_scoring_db.csv"
# Read by the website
MENS_TEAM_SCORING_DB_FILENAME = OUTPUT_PREFIX + "mens_team_scoring_db.csv"
WOMENS_TEAM_SCORING_DB_FILENAME = OUTPUT_PREFIX + "womens_team_scoring_db.csv"

TEAM_BREAKDOWN_DB_FILENAME = OUTPUT_PREFIX + "team_breakdown_db.csv"

WATCHLIST_FILENAME = OUTPUT_PREFIX + "watchlist.csv"

USPORTS_SWIMMER_ID_DATABASE_FILENAME = OUTPUT_PREFIX + "USPORTSSwimmerIDDatabase.csv"   # Not currently used

INELIGIBLE_SWIMMERS_IDS = {
    "DOMMANN, Raben_2001-02-09 00:00:00", #UBC out of eligibility
}
