### IMPORTS AND GLOBALS ###
## RUN MODE VARIABLES
RUN_MODE_CANADA_WEST = "Canada West"
RUN_MODE_USPORTS = "U SPORTS"
RUN_MODE_MCGILL = "McGill"
RUN_MODE = RUN_MODE_USPORTS

## IMPORTS
import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
import random

## CODE TO MAKE IT WORK IN 2025/2026
def build_swimrankings_session():
    s = requests.Session()

    # Match your real browser headers (from the working curl)
    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/142.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
                  "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Upgrade-Insecure-Requests": "1",
    })

    # IMPORTANT: paste your **current** cookies from the working curl here.
    # At minimum, keep cf_clearance + PHPSESSID. These are examples/placeholder values.
    s.cookies.update({
        "PHPSESSID": "cgd10ma1t9ldumfk6n3s7da2hu",
        "cf_clearance": "CLNb3jlMOf8OUZL2KTm2zEC5kvZEnl8cjlHRdm6O..4-1764031076-1.2.1.1-AdlG7uz1LHEKDidk1mffi3hcBaCHfOQwGt7vNLHW7vXEfHDNwz7huWmPy4a92Ko9blwLvQ3o9WgBKj3dmv3d88IRAQ3WgBlhsPIbUQpm1hjKgP3pXmc_TNF_5QTkDdZw2HfdhIyk0Z.B5UUxEIczSlEsr1QvTpv64Ch7ob9kL6uYoM6P4w8RDNQYdabBQAJ7HGMcr9ewHRsKWZewF6V3mJRVaUNX5ilLFHLJEp9r6zo",
        "accept-tracking": "1",
        "shw": "1600:2560",
        # _ga etc are optional; you can include them if you want
        # "_ga": "GA1.1.72842532.1701351425",
    })

    return s

SWIMRANKINGS_SESSION = build_swimrankings_session()

def safe_get(url, session=SWIMRANKINGS_SESSION, label=""):
    resp = session.get(url, timeout=30)
    if resp.status_code == 200:
        print(f"Successfully loaded page {label or ''} -> {url}")
        return resp
    elif resp.status_code == 503:
        # Hard fail so you notice it's a block and not “empty” data
        raise RuntimeError(
            f"Got 503 from Swimrankings on {label or url}. "
            "Cloudflare is blocking you again – refresh cf_clearance / cookies from your browser."
        )
    else:
        raise RuntimeError(
            f"Failed to load page {label or ''} -> {url} "
            f"(status {resp.status_code})"
        )


## GLOBALS
if RUN_MODE == RUN_MODE_USPORTS:
    DICT_OF_TEAMS_BY_CONFERENCE = {
        # ATLANTIC UNIVERSITY SPORT
        "AUS":
        [
        #"Acadia University",                    # NOT UPDATED FOR 2025/2026 - CHECK BACK
        "Dalhousie University",                 # Current
        #"Memorial University of Newfoundland",  # NOT UPDATED FOR 2025/2026 - CHECK BACK
        #"Université de Moncton",
        #"Mount Allison University",             # NOT UPDATED FOR 2025/2026 - CHECK BACK
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

        # RÉSEAU DU SPORT ÉTUDIANT DU QUÉBEC
        "RSEQ":
        [
        "Université Laval",
        "McGill University",
        "Université de Montréal",
        "University of Ottawa/Université d'Ottawa", # Current
        "Université du Québec à Trois-Rivières",
        "Université de Sherbrooke"
        ]
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

# McGill Version
elif RUN_MODE == RUN_MODE_MCGILL:
    DICT_OF_TEAMS_BY_CONFERENCE = {
        # RÉSEAU DU SPORT ÉTUDIANT DU QUÉBEC
        "RSEQ":
        [
        "McGill University"
        ]
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
SWIMRANKINGS_GENDER_STEM = "&gender="

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
        "4 x 100m Medley"
    ]
}

LIST_OF_SCORED_RELAY_EVENTS = ["4 x 100m Freestyle", "4 x 100m Medley"]

CONFERENCES = DICT_OF_TEAMS_BY_CONFERENCE.keys()

SWIMRANKINGS_CLUB_STEM = "https://www.swimrankings.net/index.php?page=rankingDetail&club=CAN."

if RUN_MODE == RUN_MODE_USPORTS:
    TEAM_TO_SWIMRANKINGS_CLUB = {
        #"Acadia University" : "ACAD",                   # NOT UPDATED FOR 2025/2026 - CHECK BACK
        "Dalhousie University" : "DAL",                 # Current
        #"Memorial University of Newfoundland" : "MUSC", # NOT UPDATED FOR 2025/2026 - CHECK BACK
        #"Université de Moncton" : None,
        #"Mount Allison University" : "MTA",             # NOT UPDATED FOR 2025/2026 - CHECK BACK
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
        "University of Ottawa/Université d'Ottawa" : "OTT", # Current
        "Queen's University" : "QUE",                   # Current
        "University of Toronto" : "UT",                 # Current
        #"Trent University" : "TRE",                    
        "University of Waterloo" : "WAT",               # Current
        "Western University" : "WES",                   # Current
        "Wilfrid Laurier University" : "WLU",           # Current
        "York University" : "YU",                       # Current
        "Université Laval" : "ULAVAL",                  # Current
        "McGill University" : "MCGILL",                 # Current
        "Université de Montréal" : "UDEM",              # Current
        "Université du Québec à Trois-Rivières" : "UQTR",   # Current
        "Université de Sherbrooke"  : "USHER"           # Current
    }
    SWIMRANKINGS_CLUB_TO_TEAM = {
        #"ACAD": "Acadia University",   # NOT UPDATED FOR 2025/2026 - CHECK BACK
        "DAL": "Dalhousie University",
        #"MUSC": "Memorial University of Newfoundland", # NOT UPDATED FOR 2025/2026 - CHECK BACK
        # "None": "Université de Moncton",
        #"MTA": "Mount Allison University", # NOT UPDATED FOR 2025/2026 - CHECK BACK
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
        "OTT": "University of Ottawa/Université d'Ottawa",
        "UNB": "University of New Brunswick",
        "QUE": "Queen's University",
        "UT": "University of Toronto",
        # "TRE": "Trent University",
        "WAT": "University of Waterloo",
        "WES": "Western University",
        "WLU": "Wilfrid Laurier University",
        "YU": "York University",
        "ULAVAL": "Université Laval",
        "MCGILL": "McGill University",
        "UDEM": "Université de Montréal",
        "UQTR": "Université du Québec à Trois-Rivières",
        "USHER": "Université de Sherbrooke"
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

SLEEP_TIME_PER_EVENT_PAGE = 6

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

CLUB_RESULTS_URL_PREFIX = "https://www.swimrankings.net/index.php?page=athleteDetail&athleteId="
CLUB_RESULTS_URL_SUFFIX = "&pbest=" + str(USPORTS_YEAR)

EXEMPT_IDS = []
#EXEMPT_IDS = ["4342739", "5627823", "4786149", "5339517", "4073747"]
EXEMPT_IDS = ["5492416", "5753229", "4908307", "5394238", "5029821", "5532239", "5192697"]  # Foreign kids that don't have Swimrankings Athlete page functionality

DO_NOT_COLLECT_IDS = ["4454358", "4596667", "4570202"]  # Finlay Knox, Blake Tierney, Hugh McNeill

### CLASSES AND METHODS ###
def load_progress_tracker(filename):
    try:
        with open(filename, "r") as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()

def save_to_progress_tracker(filename, club_name):
    with open(filename, "a") as file:
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

    for usports_team in USPORTS_TEAMS:
        tracked_progress = load_progress_tracker(PROGRESS_TRACKER_FILENAME)
        if usports_team in tracked_progress:
            continue

        for gender_int in GENDER_INTS:
            swimrankings_club = TEAM_TO_SWIMRANKINGS_CLUB[usports_team]
            swimrankings_club_ranking_url = SWIMRANKINGS_CLUB_STEM + swimrankings_club + SWIMRANKINGS_GENDER_STEM + str(gender_int)

            # Load Top Times Page
            #response = requests.get(swimrankings_club_ranking_url)

            ## NEW CODE TRIAL
            response = safe_get(
                swimrankings_club_ranking_url,
                session=SWIMRANKINGS_SESSION,
                label=f"club top times {swimrankings_club} gender={gender_int}",
            )

            ## NEW CODE TRIAL






            if response.status_code == 200:
                print("Successfully loaded page for " + swimrankings_club)
            elif response.status_code == 503:
                print("Swimrankings down for maintenance on " + swimrankings_club)
            else:
                print("Failed to load the page for " + swimrankings_club)
            sleep(SLEEP_TIME_PER_EVENT_PAGE)

            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Get Event Links
            event_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if "rankingDetail&rankingClubId=" in href:
                    event_links.append("https://www.swimrankings.net/" + href)

            print(event_links)
            
            # Go to Each Event Page
            for event_link in event_links:
                #response = requests.get(event_link)

                ## NEW CODE TRIAL
                response = safe_get(
                        event_link,
                        session=SWIMRANKINGS_SESSION,
                        label=f"event page {event_link}",
                    )

                ## NEW CODE TRIAL

                if response.status_code == 200:
                    print(f"Successfully loaded the event page: {event_link}")
                else:
                    print(f"Failed to load the event page: {event_link}")
                sleep(SLEEP_TIME_PER_EVENT_PAGE)

                # Parse the event page
                soup = BeautifulSoup(response.content, 'html.parser')

                # Get Gender, Event, Course
                gender = ""
                event_name = ""
                course_type = ""

                # Locate the table that contains the gender, event, and course information
                table = soup.find('table', {'width': '750'})

                if table:
                    rows = table.find_all('tr')

                    # Extract Course from the first row's third <td>
                    course_type = rows[1].find_all('td')[1].get_text(strip=True)  # Example: "Short Course (25m)"

                    # Extract Gender from the second row's first <td>
                    gender_text = rows[2].find_all('td')[0].get_text(strip=True)  # Example: "Men, Open" or "Women, Open"
                    gender = gender_text.split(",")[0]  # "Men" or "Women"

                    # Extract Event from the second row's second <td>
                    event_name = rows[2].find_all('td')[1].get_text(strip=True)  # Example: "50m Freestyle"

                #print(swimrankings_club + " " + gender + "'s " + event_name + " " + course_type)

                # Find and extract athlete IDs
                athlete_ids_from_event = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if "athleteDetail&athleteId=" in href:
                        athlete_id = href.split('athleteId=')[-1]
                        athlete_ids_from_event.append((athlete_id, swimrankings_club))

                athlete_ids.extend(athlete_ids_from_event)

                # Remove duplicates by converting the list to a set
                #athlete_ids = list(set(athlete_ids))

                # Store Results by Gender / Event / Course
                # Find the table containing the results
                table = soup.find('table', {'class': 'rankingList'})

                # Loop through the rows of the table (skipping header row)
                athlete_id_i = 0
                for row in table.find_all('tr')[2:]:
                    # Extract the columns in the current row
                    cols = row.find_all('td')

                    if athlete_id_i >= len(athlete_ids_from_event):
                        continue
                    
                    if len(cols) > 1:
                        # Get the Athlete ID
                        athlete_id = athlete_ids_from_event[athlete_id_i][0]

                        if (athlete_id) not in DO_NOT_COLLECT_IDS:
                            athlete_team_long = SWIMRANKINGS_CLUB_TO_TEAM[swimrankings_club]
                            athlete_conference = TEAMS_TO_CONFERENCES[athlete_team_long]

                            # Extract the swimmer's name (Lastname, firstname)
                            name = cols[0].get_text(strip=True)
                            name = name.encode('utf-8').decode('utf-8')
                            name = name.replace(',', '')

                            # Extract the time (as string)
                            swim_time = cols[4].get_text(strip=True)
                            if ("M" in swim_time):
                                swim_time = swim_time.replace('M', '')
                            fina_points = cols[5].get_text(strip=True)

                            # Add the result to the results_db as a list
                            results_list = [athlete_id, gender, event_name, course_type, swimrankings_club, athlete_conference, name, timeToSec(swim_time), fina_points]
                            results_db.append(results_list)
                    athlete_id_i += 1

        results_df = pd.DataFrame(results_db, columns=['Athlete ID', 'Gender', 'Event', 'Course', 'Team', 'Conference', 'Name', 'Time', 'AQUA'])
        results_df.to_csv(RESULTS_DB_FILENAME, index=False)
        print()

        #print(athlete_ids)
        athlete_ids_df = pd.DataFrame(athlete_ids, columns=['Athlete ID', 'Team'])
        athlete_ids_df.to_csv(ATHLETE_IDS_FILENAME, index=False)
        print()

        save_to_progress_tracker(PROGRESS_TRACKER_FILENAME, usports_team)

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
    with open(filename, "a") as file:
        file.write(athlete_id + "\n")

def GenerateClubResultsDatabase():
    # Get Previous Data
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

    club_results_db = []
    try:
        with open(CLUB_RESULTS_DB_FILENAME, "r") as file:
            reader = csv.reader(file)
            next(reader)
            club_results_db = [row for row in reader]
            print("Loaded Club Results DB")
    except FileNotFoundError:
        club_results_db = []
        print("Could not load Club Results DB")

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

    for athlete_id_row in athlete_ids:
        athlete_id = athlete_id_row[0]
        tracked_club_athlete_ids = load_club_progress_tracker(CLUB_PROGRESS_TRACKER_FILENAME)
        if athlete_id in tracked_club_athlete_ids:
            continue

        if athlete_id in EXEMPT_IDS:
            tracked_club_athlete_ids.append([athlete_id])
            club_athlete_ids_df = pd.DataFrame(tracked_club_athlete_ids, columns=['Athlete_ID'])
            club_athlete_ids_df.to_csv(CLUB_ATHLETE_IDS_FILENAME, index=False)
            continue

        if athlete_id in DO_NOT_COLLECT_IDS:
            continue

        for results_row in results_db:
            # ['Athlete ID', 'Gender', 'Event', 'Course', 'Team', 'Conference', 'Name', 'Time', 'AQUA'])
            athlete_id_from_db = results_row[0]
            gender_from_db = results_row[1]
            team_from_db = results_row[4]
            conference_from_db = results_row[5]
            name_from_db = results_row[6]

            if athlete_id_from_db == athlete_id:
                confirmed_athlete_id = athlete_id_from_db
                confirmed_gender = gender_from_db
                confirmed_team = team_from_db
                confirmed_conference = conference_from_db
                confirmed_name = name_from_db
                print("Processing " + confirmed_name + " (ID #" + str(confirmed_athlete_id) + ") from " + confirmed_team)
                break
            else:
                continue

        club_results_url = CLUB_RESULTS_URL_PREFIX + confirmed_athlete_id + CLUB_RESULTS_URL_SUFFIX
        #response = requests.get(club_results_url)

        ## NEW CODE TRIAL

        response = safe_get(
            club_results_url,
            session=SWIMRANKINGS_SESSION,
            label=f"athlete {confirmed_athlete_id} club PBs",
        )

        ## NEW CODE TRIAL

        if response.status_code == 200:
            print("Successfully loaded page for " + club_results_url)
        else:
            print("Failed to load the page for " + club_results_url)
        sleep(SLEEP_TIME_PER_EVENT_PAGE)

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Parse Soup to Get Results
        table = soup.find('table', class_='athleteBest')
        if table:
            rows0 = table.find_all('tr', class_='athleteBest0')
            rows1 = table.find_all('tr', class_='athleteBest1')
            rows = rows0 + rows1
        else:
            quit()
        
        # Extract relevant data from each column
        for row in rows:
            columns = row.find_all('td')
            event = columns[0].get_text(strip=True)
            course = columns[1].get_text(strip=True)
            swim_time = columns[2].get_text(strip=True)
            pts = columns[3].get_text(strip=True)
            date = columns[4].get_text(strip=True)
            city = columns[5].get_text(strip=True)
            meet = columns[6].get_text(strip=True)

            if course == "25m":
                course = COURSE_SCM
            elif course == "50m":
                course = COURSE_LCM
        
            # ['Athlete ID', 'Gender', 'Event', 'Course', 'Team', 'Conference', 'Name', 'Time', 'AQUA'])
            row_data = [confirmed_athlete_id, confirmed_gender, event, course, confirmed_team, confirmed_conference, confirmed_name, timeToSec(swim_time), pts]
            club_results_db.append(row_data)
        print("done")

        print("writing")
        club_results_df = pd.DataFrame(club_results_db, columns=['Athlete ID', 'Gender', 'Event', 'Course', 'Team', 'Conference', 'Name', 'Time', 'AQUA'])
        club_results_df.to_csv(CLUB_RESULTS_DB_FILENAME, index=False)

        tracked_club_athlete_ids.append([athlete_id])
        club_athlete_ids_df = pd.DataFrame(tracked_club_athlete_ids, columns=['Athlete_ID'])
        club_athlete_ids_df.to_csv(CLUB_ATHLETE_IDS_FILENAME, index=False)

        save_to_club_progress_tracker(CLUB_PROGRESS_TRACKER_FILENAME, athlete_id)
        print("wrote")
        print()

    return club_results_db

### MAIN SECTION ###

## Step 0: See if there has been any progress made... If there is, start there.
## Step 1: Get a list of U SPORTS swimmers
results_db, athlete_ids = GenerateResultsDatabase()

## Step 2: Output to CSV Files
results_df = pd.DataFrame(results_db, columns=['Athlete ID', 'Gender', 'Event', 'Course', 'Team', 'Conference', 'Name', 'Time', 'AQUA'])
results_df.to_csv(RESULTS_DB_FILENAME, index=False)

athlete_ids_df = pd.DataFrame(athlete_ids, columns=['Athlete_ID', 'Team'])
athlete_ids_df.to_csv(ATHLETE_IDS_FILENAME, index=False)
print("Varsity Results Database Created")

## Step 2.5 (Dec 16th, 2024 - Jan 25th, 2024): Get Club Results. Not every swimmer always represents their varsity tag, so we use their Swimrankings ID to get their PBs from this season.
print("Generating Club Database")
club_results_db = GenerateClubResultsDatabase()
print("Club Results Database Generated")

## Step 2.75 (Jan 25th, 2024): Update Results with Club Results
# Load varsity results
with open(RESULTS_DB_FILENAME, 'r') as file:
    reader = csv.reader(file)
    varsity_header = next(reader)  # Save header
    varsity_df = [row for row in reader]

# Load club results
with open(CLUB_RESULTS_DB_FILENAME, 'r') as file:
    reader = csv.reader(file)
    club_header = next(reader)  # Save header (assumes same format)
    club_df = [row for row in reader]

# Convert varsity_df into a dictionary for quick lookup
varsity_results = {
    (row[0], row[1], row[2], row[3]): row
    for row in varsity_df
}

# Convert club_df into a dictionary for quick lookup
club_results = {
    (row[0], row[1], row[2], row[3]): row
    for row in club_df
}

# Process varsity_df and create combined_df
combined_df = []

for key, varsity_row in varsity_results.items():
    if key in club_results:
        club_row = club_results[key]

        # If a club result exists and is faster, use it; otherwise, keep varsity result
        if club_row and float(club_row[7]) < float(varsity_row[7]):  # Compare "Time" (column index 6)
            combined_df.append(club_row)
        else:
            combined_df.append(varsity_row)
    else:
        combined_df.append(varsity_row)

# Add club-only events (i.e., events not found in varsity_df)
for key, club_row in club_results.items():
    if key not in varsity_results:  # If the event was never done in varsity meets
        combined_df.append(club_row)

# Save combined results
with open(COMBINED_RESULTS_DB_FILENAME, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(varsity_header)  # Write header
    writer.writerows(combined_df)    # Write updated results

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
with open(EVENT_SCORING_DB_FILENAME, 'w', newline='') as file:
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

## Step 3: Provide Individual Events Re-Ranking and Re-Scoring
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
            points *= 2

        row.append(points)
    else:
        row.append(0)
    
    row.append(group_str)
    
# Save restricted_event_scoring_df to a new CSV
with open(RESTRICTED_EVENT_SCORING_DB_FILENAME, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Athlete ID", "Gender", "Event", "Course", "Team", "Conference", "Name", "Time", "AQUA", "Old Place", "Old Score", "Group", "New Place", "New Score"])  # Header
    writer.writerows(rescored_df)

## Step 4: Provide Team Events Scoring
# Step 5: Load event_scoring_df into team_scoring_df
with open(RESTRICTED_EVENT_SCORING_DB_FILENAME, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    team_scoring_df = [row for row in reader]

# Step 6: Aggregate scores by team
CLUB_EVENT_TOTAL = "TOTAL"
club_scores = {}
mens_club_scores = {}
womens_club_scores = {}

for row in team_scoring_df:
    gender = row[1]
    event = row[2]
    club = row[4]
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
with open(TEAM_SCORING_DB_FILENAME, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['Rank', 'Team', 'Score'])
    
    # Write the rows with rank prepended
    for rank, club, score in ranked_clubs_with_scores_with_ranks:
        writer.writerow([rank, club, score])

# Open the CSV file in write mode
with open(MENS_TEAM_SCORING_DB_FILENAME, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['Rank', 'Team', 'Score'])
    
    # Write the rows with rank prepended
    for rank, club, score in ranked_mens_clubs_with_scores_with_ranks:
        writer.writerow([rank, club, score])

# Open the CSV file in write mode
with open(WOMENS_TEAM_SCORING_DB_FILENAME, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['Rank', 'Team', 'Score'])
    
    # Write the rows with rank prepended
    for rank, club, score in ranked_womens_clubs_with_scores_with_ranks:
        writer.writerow([rank, club, score])

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

# Step 9: Prepare the breakdown data for CSV
breakdown_data = []
for club, group_scores in club_group_scores.items():
    for group_event, score in group_scores.items():
        breakdown_data.append([club, group_event, score])

# Step 10: Write the breakdown data to TEAM_BREAKDOWN_DB_FILENAME
with open(TEAM_BREAKDOWN_DB_FILENAME, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['Team', 'Category', 'Score'])
    
    # Write the breakdown rows
    writer.writerows(breakdown_data)

print("Done!")
