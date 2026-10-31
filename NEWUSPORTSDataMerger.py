### This file was created on February 24th, 2026 to facilitate the Merge method of U SPORTS rankings.
### IMPORTS AND GLOBALS ###
## RUN MODE VARIABLES
RUN_MODE_CANADA_WEST = "Canada West"
RUN_MODE_USPORTS = "U SPORTS"
RUN_MODE_MCGILL = "McGill"
RUN_MODE = RUN_MODE_USPORTS

## IMPORTS
import pandas as pd
import csv
import os
import glob

## GLOBALS
if RUN_MODE == RUN_MODE_USPORTS:
    DICT_OF_TEAMS_BY_CONFERENCE = {
        # ATLANTIC UNIVERSITY SPORT
        "AUS":
        [
        #"Acadia University",                   # RIP
        "Dalhousie University",                 # Current
        "Memorial University of Newfoundland",  # Current
        #"Universite de Moncton",
        "Mount Allison University",             # Current
        "University of New Brunswick",          # Current
        #"University of Prince Edward Island"
        ],

        # CANADA WEST
        "CW":
        [
        #"University of Alberta",               # RIP
        "University of British Columbia",       # Current
        "University of Calgary",                # Current
        "University of Lethbridge",             # Current
        "University of Manitoba",               # Current
        "University of Regina",                 # Current
        "University of Victoria"                # Current
        ],

        # ONTARIO UNIVERSITY ATHLETICS
        "OUA":
        [
        "Brock University",                     # Current
        "Carleton University",                  # Current
        "University of Guelph",                 # Current
        #"Laurentian University",
        "McMaster University",                  # Current
        "Queen's University",                   # Current
        "University of Toronto",                # Current
        #"Trent University",                    # NOT CURRENT
        "University of Waterloo",               # Current
        "Western University",                   # Current
        "Wilfrid Laurier University",           # Current
        "York University"                       # Current
        ],

        # ReSEAU DU SPORT eTUDIANT DU QUeBEC
        "RSEQ":
        [
        "Universite Laval",
        "McGill University",
        "Universite de Montreal",
        "University of Ottawa/Universite d'Ottawa", # Current
        "Universite du Quebec a Trois-Rivieres",
        "Universite de Sherbrooke"
        ]
    }

    DICT_OF_CONFERENCES_BY_TEAM = {
        # ATLANTIC UNIVERSITY SPORT
        "Acadia University" : "AUS",
        "Dalhousie University" : "AUS",
        "Memorial University of Newfoundland" : "AUS",
        "Universite de Moncton" : "AUS",
        "Mount Allison University" : "AUS",
        "University of New Brunswick" : "AUS",
        "University of Prince Edward Island" : "AUS",

        # CANADA WEST
        "University of Alberta" : "CW",
        "University of British Columbia" : "CW",
        "University of Calgary" : "CW",
        "University of Lethbridge" : "CW",
        "University of Manitoba" : "CW",
        "University of Regina" : "CW",
        "University of Victoria" : "CW",

        # ONTARIO UNIVERSITY ATHLETICS
        "Brock University" : "OUA",
        "Carleton University" : "OUA",
        "University of Guelph" : "OUA",
        "Laurentian University" : "OUA",
        "McMaster University" : "OUA",
        "Queen's University" : "OUA",
        "University of Toronto" : "OUA",
        "Trent University" : "OUA",
        "University of Waterloo" : "OUA",
        "Western University" : "OUA",
        "Wilfrid Laurier University" : "OUA",
        "York University" : "OUA",

        # ReSEAU DU SPORT eTUDIANT DU QUeBEC
        "Universite Laval" : "RSEQ",
        "McGill University" : "RSEQ",
        "Universite de Montreal" : "RSEQ",
        "University of Ottawa/Universite d'Ottawa" : "RSEQ",
        "Universite du Quebec a Trois-Rivieres" : "RSEQ",
        "Universite de Sherbrooke" : "RSEQ"
    }

# Canada West Version
elif RUN_MODE == RUN_MODE_CANADA_WEST:
    DICT_OF_TEAMS_BY_CONFERENCE = {
        # CANADA WEST
        "CW":
        [
        #"University of Alberta",           # RIP
        "University of British Columbia"
        "University of Calgary",
        "University of Lethbridge",
        "University of Manitoba",
        "University of Regina",
        "University of Victoria"
        ]
    }

    DICT_OF_CONFERENCES_BY_TEAM = {
        # CANADA WEST
        "University of Alberta" : "CW",
        "University of British Columbia" : "CW",
        "University of Calgary" : "CW",
        "University of Lethbridge" : "CW",
        "University of Manitoba" : "CW",
        "University of Regina" : "CW",
        "University of Victoria" : "CW",
    }

# McGill Version
elif RUN_MODE == RUN_MODE_MCGILL:
    DICT_OF_TEAMS_BY_CONFERENCE = {
        # ReSEAU DU SPORT eTUDIANT DU QUeBEC
        "RSEQ":
        [
        "McGill University"
        ]
    }

    DICT_OF_CONFERENCES_BY_TEAM = {
        # ReSEAU DU SPORT eTUDIANT DU QUeBEC
        "McGill University" : "RSEQ"
    }

TEAMS_TO_CONFERENCES = {}
for conference in DICT_OF_TEAMS_BY_CONFERENCE:
    for team in DICT_OF_TEAMS_BY_CONFERENCE[conference]:
        TEAMS_TO_CONFERENCES[team] = conference

GENDER_MEN = "Men"
GENDER_WOMEN = "Women"
GENDERS = ["Men", "Women"]

GENDER_MEN_INT = "1"
GENDER_WOMEN_INT = "2"
GENDER_INTS = [GENDER_MEN_INT, GENDER_WOMEN_INT]

LIST_OF_SCORING_EVENTS_BY_GENDER = {
    GENDER_MEN : [
        "50m Freestyle",
        "100m Freestyle",
        "200m Freestyle",
        "400m Freestyle",
        "1500m Freestyle",
        "50m Butterfly",
        "100m Butterfly",
        "200m Butterfly",
        "50m Backstroke",
        "100m Backstroke",
        "200m Backstroke",
        "50m Breaststroke",
        "100m Breaststroke",
        "200m Breaststroke",
        "200m Medley",
        "400m Medley",
        "4 x 100m Freestyle",
        "4 x 200m Freestyle",
        "4 x 100m Medley"
    ],
    GENDER_WOMEN : [
        "50m Freestyle",
        "100m Freestyle",
        "200m Freestyle",
        "400m Freestyle",
        "800m Freestyle",
        "50m Butterfly",
        "100m Butterfly",
        "200m Butterfly",
        "50m Backstroke",
        "100m Backstroke",
        "200m Backstroke",
        "50m Breaststroke",
        "100m Breaststroke",
        "200m Breaststroke",
        "200m Medley",
        "400m Medley",
        "4 x 100m Freestyle",
        "4 x 200m Freestyle",
        "4 x 100m Medley"
    ]
}

LONG_EVENT_TO_SHORT_EVENT = {
        "50m Freestyle" : "50m Fr",
        "100m Freestyle" : "100m Fr",
        "200m Freestyle" : "200m Fr",
        "400m Freestyle" : "400m Fr",
        "800m Freestyle" : "800m Fr",
        "1500m Freestyle" : "1500m Fr",
        "50m Butterfly" : "50m Bu",
        "100m Butterfly" : "100m Bu",
        "200m Butterfly" : "200m Bu",
        "50m Backstroke" : "50m Bk",
        "100m Backstroke" : "100m Bk",
        "200m Backstroke" : "200m Bk",
        "50m Breaststroke" : "50m Br",
        "100m Breaststroke" : "100m Br",
        "200m Breaststroke" : "200m Br",
        "200m Medley" : "200m Me",
        "400m Medley" : "400m Me",
        "4 x 100m Freestyle" : "4 x 100m Fr",
        "4 x 200m Freestyle" : "4 x 200m Fr",
        "4 x 100m Medley" : "4 x 100m Me"
}

SHORT_EVENT_TO_LONG_EVENT = {
    "50m Fr": "50m Freestyle",
    "100m Fr": "100m Freestyle",
    "200m Fr": "200m Freestyle",
    "400m Fr": "400m Freestyle",
    "800m Fr": "800m Freestyle",
    "1500m Fr": "1500m Freestyle",
    "50m Bu": "50m Butterfly",
    "100m Bu": "100m Butterfly",
    "200m Bu": "200m Butterfly",
    "50m Bk": "50m Backstroke",
    "100m Bk": "100m Backstroke",
    "200m Bk": "200m Backstroke",
    "50m Br": "50m Breaststroke",
    "100m Br": "100m Breaststroke",
    "200m Br": "200m Breaststroke",
    "200m Me": "200m Medley",
    "400m Me": "400m Medley",
    "4 x 100m Fr": "4 x 100m Freestyle",
    "4 x 200m Fr": "4 x 200m Freestyle",
    "4 x 100m Me": "4 x 100m Medley"
}

LIST_OF_SCORED_RELAY_EVENTS = ["4 x 100m Freestyle", "4 x 200m Freestyle", "4 x 100m Medley"]

CONFERENCES = DICT_OF_TEAMS_BY_CONFERENCE.keys()

if RUN_MODE == RUN_MODE_USPORTS:
    TEAM_TO_SWIMRANKINGS_CLUB = {
        #"Acadia University" : "ACAD",                   # RIP
        "Dalhousie University" : "DAL",                 # Current
        "Memorial University of Newfoundland" : "MUSC", # Current
        #"Universite de Moncton" : None,
        "Mount Allison University" : "MTA",             # Current
        #"University of Prince Edward Island" : None,
        #"University of Alberta" : "UOFA",              # RIP
        "University of British Columbia" : "UBCT",      # Current
        "University of Calgary" : "UOFC",               # Current
        "University of Lethbridge" : "UOFL",            # Current
        "University of Manitoba" : "UM",                # Current
        "University of Regina" : "UOFR",                # Current
        "University of Victoria" : "UVIC",              # Current
        "Brock University" : "BADGR",                   # Current
        "Carleton University" : "CAR",                  # Current
        "University of Guelph" : "UG",                  # Current
        #"Laurentian University" : "LU",
        "McMaster University" : "MACU",                 # Current
        "University of New Brunswick" : "UNB",          # Current
        "University of Ottawa/Universite d'Ottawa" : "OTT", # Current
        "Queen's University" : "QUE",                   # Current
        "University of Toronto" : "UT",                 # Current
        #"Trent University" : "TRE",                    
        "University of Waterloo" : "WAT",               # Current
        "Western University" : "WES",                   # Current
        "Wilfrid Laurier University" : "WLU",           # Current
        "York University" : "YU",                       # Current
        "Universite Laval" : "ULAVAL",                  # Current
        "McGill University" : "MCGILL",                 # Current
        "Universite de Montreal" : "UDEM",              # Current
        "Universite du Quebec a Trois-Rivieres" : "UQTR",   # Current
        "Universite de Sherbrooke"  : "USHER"           # Current
    }
    SWIMRANKINGS_CLUB_TO_TEAM = {
        "ACAD": "Acadia University",   # RIP
        "DAL": "Dalhousie University",
        "MUSC": "Memorial University of Newfoundland", # Current
        # "None": "Universite de Moncton",
        "MTA": "Mount Allison University", # Current
        # "None": "University of Prince Edward Island",
        # "UOFA": "University of Alberta",
        "UBCT": "University of British Columbia",
        "UOFC": "University of Calgary",
        "UOFL": "University of Lethbridge",
        "UM": "University of Manitoba",
        "UOFR": "University of Regina",
        "UVIC": "University of Victoria",
        "BADGR": "Brock University",
        "CAR": "Carleton University",
        "UG": "University of Guelph",
        # "LU": "Laurentian University",
        "MACU": "McMaster University",
        "UNB": "University of New Brunswick",
        "QUE": "Queen's University",
        "UT": "University of Toronto",
        # "TRE": "Trent University",
        "WAT": "University of Waterloo",
        "WES": "Western University",
        "WLU": "Wilfrid Laurier University",
        "YU": "York University",
        "OTT": "University of Ottawa/Universite d'Ottawa",
        "ULAVAL": "Universite Laval",
        "MCGILL": "McGill University",
        "UDEM": "Universite de Montreal",
        "UQTR": "Universite du Quebec a Trois-Rivieres",
        "USHER": "Universite de Sherbrooke"
    }

elif RUN_MODE == RUN_MODE_CANADA_WEST:
    # Canada West Version
    TEAM_TO_SWIMRANKINGS_CLUB = {
        #"University of Alberta" : "UOFA",
        "University of British Columbia" : "UBCT",
        "University of Calgary" : "UOFC",
        "University of Lethbridge" : "UOFL",
        "University of Manitoba" : "UM",
        "University of Regina" : "UOFR",
        "University of Victoria" : "UVIC",
    }

    SWIMRANKINGS_CLUB_TO_TEAM = {
    #"UOFA": "University of Alberta",
    "UBCT": "University of British Columbia",
    "UOFC": "University of Calgary",
    "UOFL": "University of Lethbridge",
    "UM": "University of Manitoba",
    "UOFR": "University of Regina",
    "UVIC": "University of Victoria"
    }

elif RUN_MODE == RUN_MODE_MCGILL:
    TEAM_TO_SWIMRANKINGS_CLUB = {
        "McGill University" : "MCGILL",                 # Current
    }
    SWIMRANKINGS_CLUB_TO_TEAM = {
        "MCGILL": "McGill University"
    }


USPORTS_TEAMS = TEAM_TO_SWIMRANKINGS_CLUB.keys()

OUTPUT_PREFIX = "OUTPUT_"

USPORTS_SWIMMER_ID_DATABASE_FILENAME = OUTPUT_PREFIX + "USPORTSSwimmerIDDatabase.csv"
USPORTS_YEAR = "2026"

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

COURSE_SCM = "Short Course (25m)"
COURSE_LCM = "Long Course (50m)"

SCORING_COURSES = [COURSE_SCM]

PROGRESS_TRACKER_FILENAME = OUTPUT_PREFIX + "progress_tracker.txt"
CLUB_PROGRESS_TRACKER_FILENAME = OUTPUT_PREFIX + "club_progress_tracker.txt"

RESULTS_DB_FILENAME = OUTPUT_PREFIX + "results_db.csv"
ATHLETE_IDS_FILENAME = OUTPUT_PREFIX + "athlete_ids.csv"

CLUB_RESULTS_DB_FILENAME = OUTPUT_PREFIX + "club_results_db.csv"
CLUB_ATHLETE_IDS_FILENAME = OUTPUT_PREFIX + "club_athlete_ids.csv"

COMBINED_RESULTS_DB_FILENAME = OUTPUT_PREFIX + "combined_results_db.csv"

EVENT_SCORING_DB_FILENAME = OUTPUT_PREFIX + "event_scoring_db.csv"
RESTRICTED_EVENT_SCORING_DB_FILENAME = OUTPUT_PREFIX + "restricted_event_scoring_db.csv"

TEAM_SCORING_DB_FILENAME = OUTPUT_PREFIX + "team_scoring_db.csv"
MENS_TEAM_SCORING_DB_FILENAME = OUTPUT_PREFIX + "mens_team_scoring_db.csv"
WOMENS_TEAM_SCORING_DB_FILENAME = OUTPUT_PREFIX + "womens_team_scoring_db.csv"

TEAM_BREAKDOWN_DB_FILENAME = OUTPUT_PREFIX + "team_breakdown_db.csv"

RELAY_START_ALLOWANCE = 0.5
SCM_TO_LCM_CONVERSION_FACTOR = 1.03
NUMBER_OF_INDIVIDUAL_EVENTS_TO_SCORE = 4

CANADA_WEST_RELAY_SCORE_MODIFIER = 2
U_SPORTS_RELAY_SCORE_MODIFIER = 1

if RUN_MODE == RUN_MODE_USPORTS:
    RELAY_SCORE_MODIFIER = U_SPORTS_RELAY_SCORE_MODIFIER # 2 for CanWest, 1 for U SPORTS
elif RUN_MODE == RUN_MODE_CANADA_WEST:
    RELAY_SCORE_MODIFIER = CANADA_WEST_RELAY_SCORE_MODIFIER
elif RUN_MODE == RUN_MODE_MCGILL:
    RELAY_SCORE_MODIFIER = U_SPORTS_RELAY_SCORE_MODIFIER

MAXIMUM_SCORED_SWIMS_PER_SWIMMER = 4
MAXIMUM_SCORED_RELAYS_PER_TEAM_AND_GENDER = 1

EXEMPT_IDS = []
#EXEMPT_IDS = ["4342739", "5627823", "4786149", "5339517", "4073747"]
EXEMPT_IDS = ["5492416", "5753229", "4908307", "5394238", "5029821", "5532239", "5192697", "4969912"]  # Foreign kids that don't have Swimrankings Athlete page functionality

DO_NOT_COLLECT_IDS = ["4454358", "4596667", "4570202"]  # Finlay Knox, Blake Tierney, Hugh McNeill

### CLASSES AND METHODS ###
def load_progress_tracker(filename):
    try:
        with open(filename, "r") as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()

def save_to_progress_tracker(filename, club_name):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(club_name + "\n")

def GenerateResultsDatabase():
    results_db = []
    try:
        with open(RESULTS_DB_FILENAME, "r") as file:
            reader = csv.reader(file)
            next(reader)
            results_db = [row for row in reader]
            print("Loaded Results DB")
    except FileNotFoundError:
        results_db = []
        print("Could not load Results DB")

    athlete_ids = []
    try:
        with open(ATHLETE_IDS_FILENAME, "r") as file:
            reader = csv.reader(file)
            next(reader)
            athlete_ids = [row for row in reader]
            print("Loaded Athlete IDs DB")
    except FileNotFoundError:
        athlete_ids = []
        print("Could not load Athlete IDs DB")

    # --- NEW SECTION START ---
    # Path to folder containing your .xlsx files
    data_folder = "./INPUT/"  # adjust if they’re in a subdirectory

    # Loop through all varsity .xlsx files (not the Canada-level ones)
    for file_path in glob.glob(os.path.join(data_folder, "CAN-*_2026_SCM_*.xlsx")):
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
                    COURSE_SCM,   # Course
                    club_code,              # Team
                    conference_name,        # Conference
                    athlete_name,           # Name
                    swimtime,               # Time
                    aqua_points             # AQUA
                ])

                athlete_ids.append([athlete_id, team_name])

        save_to_progress_tracker(PROGRESS_TRACKER_FILENAME, team_name)
        print(f"✅ Finished {team_name}\n")
    # --- NEW SECTION END ---

    results_df = pd.DataFrame(results_db, columns=['Athlete ID', 'Gender', 'Event', 'Course', 'Team', 'Conference', 'Name', 'Time', 'AQUA'])
    results_df.to_csv(RESULTS_DB_FILENAME, index=False, encoding="utf-8")
    print("Saved Results DB")

    athlete_ids_df = pd.DataFrame(athlete_ids, columns=['Athlete ID', 'Team'])
    athlete_ids_df.to_csv(ATHLETE_IDS_FILENAME, index=False)
    print("Saved Athlete IDs DB")

    return results_db, athlete_ids

def placeToPoints(p):
    points = 0
    if p in PLACE_TO_POINTS:
        points = PLACE_TO_POINTS[p]
    return points

def timeToSec(swim_time):
    """
    Converts a swimming time in (m)m:ss.hh format to total seconds.
    :param swim_time: str - Time in the format 'mm:ss.hh' or 'ss.hh'
    :return: float - Time in seconds
    """
    if ("M" in swim_time):
        swim_time = swim_time.replace('M', '')

    if ':' in swim_time:
        # If the time includes minutes
        minutes, seconds = swim_time.split(':')
        total_seconds = int(minutes) * 60 + float(seconds)
    else:
        # If the time is only in seconds
        total_seconds = float(swim_time)
    return round(total_seconds, 2)

def secToTime(seconds):
    """
    Converts time in total seconds to (m)m:ss.hh format.
    If the input time is less than 60 seconds, it remains in ss.hh format.
    :param seconds: float - Time in seconds
    :return: str - Time in the format 'mm:ss.hh' or 'ss.hh'
    """
    if seconds < 60:
        # If the total time is less than one minute, keep it in seconds format
        return f"{seconds:.2f}"
    else:
        # Otherwise, convert to mm:ss.hh
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}:{remaining_seconds:05.2f}"


def load_club_progress_tracker(filename):
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

def save_to_club_progress_tracker(filename, athlete_id):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(athlete_id + "\n")

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

    # Canadian files folder
    data_folder = "./INPUT/"

    # Identify files like CAN_2026_SCM_Men_17-99.xlsx
    canadian_files = glob.glob(os.path.join(data_folder, "CAN_2026_SCM_*_17-99.xlsx"))
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

### MAIN SECTION ###

## Step 0: See if there has been any progress made... If there is, start there.
## Step 1: Get a list of U SPORTS swimmers
results_db, athlete_ids = GenerateResultsDatabase()
print("Done Step 1/10")

## Step 2: Output to CSV Files
results_df = pd.DataFrame(results_db, columns=['Athlete ID', 'Gender', 'Event', 'Course', 'Team', 'Conference', 'Name', 'Time', 'AQUA'])
results_df.to_csv(RESULTS_DB_FILENAME, index=False, encoding="utf-8")

athlete_ids_df = pd.DataFrame(athlete_ids, columns=['Athlete_ID', 'Team'])
athlete_ids_df.to_csv(ATHLETE_IDS_FILENAME, index=False, encoding="utf-8")
print("Varsity Results Database Created")
print("Done Step 2/10")

## Step 2.5 (Dec 16th, 2024 - Jan 25th, 2024): Get Club Results. Not every swimmer always represents their varsity tag, so we use their Swimrankings ID to get their PBs from this season.
print("Generating Club Database")
club_results_db = GenerateClubResultsDatabase()
print("Club Results Database Generated")
print("Done Step 2.5/10")

## Step 2.75 (Feb 24th, 2026): Merge Club Results with Varsity Results (Varsity Team Tag Enforcement)

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
        def to_sec_safe(t):
            try:
                return timeToSec(t)
            except:
                return float("inf")

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

# Save combined results
with open(COMBINED_RESULTS_DB_FILENAME, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(varsity_header)
    writer.writerows(combined_df)

print(f"💾 Combined Results DB saved to {COMBINED_RESULTS_DB_FILENAME} ({len(combined_df)} rows)")
print("Done Step 2.75/10")

## Step 3: Provide Individual Events Filtering, Ranking, and Scoring
# Sort results by gender, event, course, and then time. Then, score them.
with open(COMBINED_RESULTS_DB_FILENAME, 'r') as file:
    reader = csv.reader(file)
    next(reader)
    event_scoring_df = [row for row in reader]

# Sort event_scoring_df by Gender, Event, Course, and then Time
event_scoring_df.sort(key=lambda x: (x[1], x[2], x[3], float(timeToSec(x[7]))))  # Assuming Time is in column 5

# Add Place and Score columns
place_col_index = len(event_scoring_df[0])  # Next column for place
score_col_index = place_col_index + 1  # Next column for score

current_group = None
place = 0

for row in event_scoring_df:
    # Group by Gender, Event, Course (columns 0, 1, 2)
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
    

# Save event_scoring_df to a new CSV
with open(EVENT_SCORING_DB_FILENAME, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Athlete ID", "Gender", "Event", "Course", "Team", "Conference", "Name", "Time", "AQUA", "Place", "Score", "Group"])  # Header
    writer.writerows(event_scoring_df)


# Load Event Scores, which are unrestricted
with open(EVENT_SCORING_DB_FILENAME, 'r') as file:
    reader = csv.reader(file)
    next(reader)
    event_scoring_df = [row for row in reader]

# Restrict the event scores by Top 4 Swims per Swimmer and Top 1 Swim per relay
# Apply filtering and rescoring
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
from operator import itemgetter

top_individual_swims = []
for individual_athlete in individual_athletes:
    athlete_swims = [row for row in event_scoring_df if row[6] == individual_athlete]
    
    # Sort by Score (Descending), then AQUA (Descending), then Time (Ascending)
    athlete_swims.sort(key=lambda x: (-float(x[10]), -float(x[8]) if x[8].replace('.', '', 1).isdigit() else 0, float(timeToSec(x[7]))))
    
    # Select Top 4 Swims
    top_individual_swims.extend(athlete_swims[:MAXIMUM_SCORED_SWIMS_PER_SWIMMER])

# Get Top 1 Swim for Each Relay
top_relay_swims = []

for team in relay_teams:
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

rescored_df = top_individual_swims + top_relay_swims

print("Done Step 3/10")

## Step 4: Provide Individual Events Re-Ranking and Re-Scoring
# Sort rescored by Gender, Event, Course, and then Time
rescored_df.sort(key=lambda x: (x[1], x[2], x[3], float(timeToSec(x[7]))))  # Assuming Time is in column 5

# Add Place and Score columns
place_col_index = len(rescored_df[0])  # Next column for place
score_col_index = place_col_index + 1  # Next column for score

current_group = None
place = 0

for row in rescored_df:
    # Group by Gender, Event, Course (columns 0, 1, 2)
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
    
# Save restricted_event_scoring_df to a new CSV
with open(RESTRICTED_EVENT_SCORING_DB_FILENAME, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Athlete ID", "Gender", "Event", "Course", "Team", "Conference", "Name", "Time", "AQUA", "Old Place", "Old Score", "Group", "New Place", "New Score"])  # Header
    writer.writerows(rescored_df)

print("Done Step 4/10")

## Step 5: Provide Team Events Scoring
# Step 5: Load event_scoring_df into team_scoring_df
with open(RESTRICTED_EVENT_SCORING_DB_FILENAME, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    team_scoring_df = [row for row in reader]

print("Done Step 5/10")

# Step 6: Aggregate scores by team
CLUB_EVENT_TOTAL = "TOTAL"
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

print("Done Step 6/10")

# Step 7: Rank the clubs by total score (using CLUB_EVENT_TOTAL)
ranked_clubs = sorted(club_scores.items(), key=lambda x: x[1].get(CLUB_EVENT_TOTAL, 0), reverse=True)
ranked_mens_clubs = sorted(mens_club_scores.items(), key=lambda x: x[1].get(CLUB_EVENT_TOTAL, 0), reverse=True)
ranked_womens_clubs = sorted(womens_club_scores.items(), key=lambda x: x[1].get(CLUB_EVENT_TOTAL, 0), reverse=True)

# If you want to display the rankings with club names and total scores:
ranked_clubs_with_scores = [(club, scores[CLUB_EVENT_TOTAL]) for club, scores in ranked_clubs]
ranked_mens_clubs_with_scores = [(club, scores[CLUB_EVENT_TOTAL]) for club, scores in ranked_mens_clubs]
ranked_womens_clubs_with_scores = [(club, scores[CLUB_EVENT_TOTAL]) for club, scores in ranked_womens_clubs]

# Add rank as the first element in each tuple
ranked_clubs_with_scores_with_ranks = [(i + 1, club, score) for i, (club, score) in enumerate(ranked_clubs_with_scores)]
ranked_mens_clubs_with_scores_with_ranks = [(i + 1, club, score) for i, (club, score) in enumerate(ranked_mens_clubs_with_scores)]
ranked_womens_clubs_with_scores_with_ranks = [(i + 1, club, score) for i, (club, score) in enumerate(ranked_womens_clubs_with_scores)]

# Open the CSV file in write mode
with open(TEAM_SCORING_DB_FILENAME, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['Rank', 'Team', 'Score', 'Conference'])
    
    # Write the rows with rank prepended
    for rank, club, score in ranked_clubs_with_scores_with_ranks:
        writer.writerow([rank, club, score, DICT_OF_CONFERENCES_BY_TEAM[SWIMRANKINGS_CLUB_TO_TEAM[club]]])

# Open the CSV file in write mode
with open(MENS_TEAM_SCORING_DB_FILENAME, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['Rank', 'Team', 'Score', 'Conference'])
    
    # Write the rows with rank prepended
    for rank, club, score in ranked_mens_clubs_with_scores_with_ranks:
        writer.writerow([rank, club, score, DICT_OF_CONFERENCES_BY_TEAM[SWIMRANKINGS_CLUB_TO_TEAM[club]]])

# Open the CSV file in write mode
with open(WOMENS_TEAM_SCORING_DB_FILENAME, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['Rank', 'Team', 'Score', 'Conference'])
    
    # Write the rows with rank prepended
    for rank, club, score in ranked_womens_clubs_with_scores_with_ranks:
        writer.writerow([rank, club, score, DICT_OF_CONFERENCES_BY_TEAM[SWIMRANKINGS_CLUB_TO_TEAM[club]]])

print("Done Step 7/10")

# Step 8: Aggregate scores by club and group
club_group_scores = {}

# Loop through team_scoring_df to aggregate scores by club and group
for row in team_scoring_df:
    gender = row[1]
    event = row[2]
    course = row[3]
    club = row[4]
    score = int(row[13])
    group = row[11]
    
    # Aggregate scores by club and group
    if event in LIST_OF_SCORING_EVENTS_BY_GENDER[gender] and course in SCORING_COURSES:
        if club in club_group_scores:
            if group in club_group_scores[club]:
                club_group_scores[club][group] += score
            else:
                club_group_scores[club][group] = score
        else:
            club_group_scores[club] = {group: score}
    else:
        continue
print("Done Step 8/10")

# Step 9: Prepare the breakdown data for CSV
breakdown_data = []
for club, group_scores in club_group_scores.items():
    for group_event, score in group_scores.items():
        breakdown_data.append([club, group_event, score])
print("Done Step 9/10")

# Step 10: Write the breakdown data to TEAM_BREAKDOWN_DB_FILENAME
with open(TEAM_BREAKDOWN_DB_FILENAME, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['Team', 'Category', 'Score'])
    
    # Write the breakdown rows
    writer.writerows(breakdown_data)

print("Done Step 10/10")
print("Done!")
