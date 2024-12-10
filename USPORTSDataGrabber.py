### IMPORTS AND GLOBALS ###
## RUN MODE VARIABLES
RUN_MODE_CANADA_WEST = "Canada West"
RUN_MODE_USPORTS = "U SPORTS"
RUN_MODE = RUN_MODE_USPORTS

## IMPORTS
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import csv
import random

## GLOBALS
if RUN_MODE == RUN_MODE_USPORTS:
    DICT_OF_TEAMS_BY_CONFERENCE = {
        # ATLANTIC UNIVERSITY SPORT
        "AUS":
        [
        "Acadia University",                    # Current
        "Dalhousie University",                 # Current
        "Memorial University of Newfoundland",  # Current
        #"Université de Moncton",
        "Mount Allison University",             # Current
        #"University of Prince Edward Island"
        ],

        # CANADA WEST
        "CW":
        [
        "University of Alberta",                # Current
        "University of British Columbia"        # Current
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
        "University of Ottawa/Université d'Ottawa", # Current
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
        "University of Alberta",
        "University of British Columbia"
        "University of Calgary",
        "University of Lethbridge",
        "University of Manitoba",
        "University of Regina",
        "University of Victoria"
        ]
    }

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
        "Acadia University" : "ACAD",                   # Current
        "Dalhousie University" : "DAL",                 # Current
        "Memorial University of Newfoundland" : "MUSC", # Current
        #"Université de Moncton" : None,
        "Mount Allison University" : "MTA",             # Current
        #"University of Prince Edward Island" : None,
        "University of Alberta" : "UOFA",               # Current
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

elif RUN_MODE == RUN_MODE_CANADA_WEST:
    # Canada West Version
    TEAM_TO_SWIMRANKINGS_CLUB = {
        "University of Alberta" : "UOFA",
        "University of British Columbia" : "UBCT",
        "University of Calgary" : "UOFC",
        "University of Lethbridge" : "UOFL",
        "University of Manitoba" : "UM",
        "University of Regina" : "UOFR",
        "University of Victoria" : "UVIC",
    }


USPORTS_TEAMS = TEAM_TO_SWIMRANKINGS_CLUB.keys()

OUTPUT_PREFIX = "OUTPUT_"

USPORTS_SWIMMER_ID_DATABASE_FILENAME = OUTPUT_PREFIX + "USPORTSSwimmerIDDatabase.csv"
USPORTS_YEAR = "2025"

USPORTS_POINTS = "TODO"

PLACE_TO_POINTS = {
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

COURSE_SCM = "Short Course (25m)"
COURSE_LCM = "Long Course (50m)"

SCORING_COURSES = [COURSE_SCM]

PROGRESS_TRACKER_FILENAME = OUTPUT_PREFIX + "progress_tracker.txt"

RESULTS_DB_FILENAME = OUTPUT_PREFIX + "results_db.csv"
ATHLETE_IDS_FILENAME = OUTPUT_PREFIX + "athlete_ids.csv"

EVENT_SCORING_DB_FILENAME = OUTPUT_PREFIX + "event_scoring_db.csv"
RESTRICTED_EVENT_SCORING_DB_FILENAME = OUTPUT_PREFIX + "restricted_event_scoring_db.csv"

TEAM_SCORING_DB_FILENAME = OUTPUT_PREFIX + "team_scoring_db.csv"
MENS_TEAM_SCORING_DB_FILENAME = OUTPUT_PREFIX + "mens_team_scoring_db.csv"
WOMENS_TEAM_SCORING_DB_FILENAME = OUTPUT_PREFIX + "womens_team_scoring_db.csv"

TEAM_BREAKDOWN_DB_FILENAME = OUTPUT_PREFIX + "team_breakdown_db.csv"

RELAY_START_ALLOWANCE = 0.5
SCM_TO_LCM_CONVERSION_FACTOR = 1.03
NUMBER_OF_INDIVIDUAL_EVENTS_TO_SCORE = 4

SLEEP_TIME_PER_EVENT_PAGE = 1
RANDOM_SLEEP_TIME_PER_EVENT_PAGE = 3

CANADA_WEST_RELAY_SCORE_MODIFIER = 2
U_SPORTS_RELAY_SCORE_MODIFIER = 1

if RUN_MODE == RUN_MODE_USPORTS:
    RELAY_SCORE_MODIFIER = U_SPORTS_RELAY_SCORE_MODIFIER # 2 for CanWest, 1 for U SPORTS
elif RUN_MODE == RUN_MODE_CANADA_WEST:
    RELAY_SCORE_MODIFIER = CANADA_WEST_RELAY_SCORE_MODIFIER

MAXIMUM_SCORED_SWIMS_PER_SWIMMER = 4
MAXIMUM_SCORED_RELAYS_PER_TEAM_AND_GENDER = 1

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
            response = requests.get(swimrankings_club_ranking_url)
            if response.status_code == 200:
                print("Successfully loaded page for " + swimrankings_club)
            else:
                print("Failed to load the page for " + swimrankings_club)
            time.sleep(SLEEP_TIME_PER_EVENT_PAGE)

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
                response = requests.get(event_link)

                if response.status_code == 200:
                    print(f"Successfully loaded the event page: {event_link}")
                else:
                    print(f"Failed to load the event page: {event_link}")
                time.sleep(SLEEP_TIME_PER_EVENT_PAGE)

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
                for row in table.find_all('tr')[2:]:
                    # Extract the columns in the current row
                    cols = row.find_all('td')
                    
                    if len(cols) > 1:
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
                        results_list = [gender, event_name, course_type, swimrankings_club, name, timeToSec(swim_time), fina_points]
                        results_db.append(results_list)

        results_df = pd.DataFrame(results_db, columns=['Gender', 'Event', 'Course', 'Team', 'Name', 'Time', 'AQUA'])
        results_df.to_csv(RESULTS_DB_FILENAME, index=False)
        print()


        #print(athlete_ids)
        athlete_ids_df = pd.DataFrame(athlete_ids, columns=['Athlete_ID', 'Team'])
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

### MAIN SECTION ###

## Step 0: See if there has been any progress made... If there is, start there.
## Step 1: Get a list of U SPORTS swimmers
results_db, athlete_ids = GenerateResultsDatabase()

## Step 2: Output to CSV Files
results_df = pd.DataFrame(results_db, columns=['Gender', 'Event', 'Course', 'Team', 'Name', 'Time', 'AQUA'])
results_df.to_csv(RESULTS_DB_FILENAME, index=False)

athlete_ids_df = pd.DataFrame(athlete_ids, columns=['Athlete_ID', 'Team'])
athlete_ids_df.to_csv(ATHLETE_IDS_FILENAME, index=False)

## Step 3: Provide Individual Events Filtering, Ranking, and Scoring
# Sort results by gender, event, course, and then time. Then, score them.
with open(RESULTS_DB_FILENAME, 'r') as file:
    reader = csv.reader(file)
    next(reader)
    event_scoring_df = [row for row in reader]

# Sort event_scoring_df by Gender, Event, Course, and then Time
event_scoring_df.sort(key=lambda x: (x[0], x[1], x[2], float(timeToSec(x[5]))))  # Assuming Time is in column 5

# Add Place and Score columns
place_col_index = len(event_scoring_df[0])  # Next column for place
score_col_index = place_col_index + 1  # Next column for score

current_group = None
place = 0

for row in event_scoring_df:
    # Group by Gender, Event, Course (columns 0, 1, 2)
    gender = row[0]
    event = row[1]
    course = row[2]

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
    

# Save event_scoring_df to a new CSV
with open(EVENT_SCORING_DB_FILENAME, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Gender", "Event", "Course", "Team", "Name", "Time", "AQUA", "Place", "Score", "Group"])  # Header
    writer.writerows(event_scoring_df)


# Load Event Scores, which are unrestricted
with open(EVENT_SCORING_DB_FILENAME, 'r') as file:
    reader = csv.reader(file)
    next(reader)
    event_scoring_df = [row for row in reader]

# Restrict the event scores by Top 4 Swims per Swimmer and Top 1 Swim per relay
# Apply filtering and rescoring
individual_athletes = []
individual_teams = []

# Get Individual Athletes and Teams
for row in event_scoring_df:
    event = row[1]
    swimmer_name = row[4]

    if ('x' not in event) and (swimmer_name not in individual_athletes):
        individual_athletes.append(swimmer_name)

    if ('x' in event) and (swimmer_name not in individual_teams):
        individual_teams.append(swimmer_name)

# Get Top 4 Swims for Each Individual
top_individual_swims = []
for individual_athlete in individual_athletes:
    swim_count = 0

    for row in event_scoring_df:
        swimmer_name = row[4]
        if swimmer_name == individual_athlete:
            swim_count += 1
    
    selected_rows = []
    if swim_count > MAXIMUM_SCORED_SWIMS_PER_SWIMMER:
        selected_rows = []
        for i in range(MAXIMUM_SCORED_SWIMS_PER_SWIMMER):
            highest_event_so_far = None
            highest_score_so_far = -1
            for row in event_scoring_df:
                swimmer_name = row[4]
                if swimmer_name == individual_athlete:
                    old_score = float(row[8])
                    event_name = row[1]
                    if (old_score >= highest_score_so_far and row not in selected_rows):
                        if ("Lap" not in event_name or ("Lap" in event_name and highest_event_so_far == None)):
                            highest_score_so_far = old_score
                            highest_event_so_far = row
            selected_rows.append(highest_event_so_far)
    else:
        # Grab them All
        for row in event_scoring_df:
            swimmer_name = row[4]
            if swimmer_name == individual_athlete:
                selected_rows.append(row)
    
    for selected_row in selected_rows:
        top_individual_swims.append(selected_row)
    
# Get Top 1 Swim for Each Relay
top_relay_swims = []
for individual_team in individual_teams:
    selected_rows = []
    seen_relays = []
    for row in event_scoring_df:
        gender = row[0]
        event = row[1]
        team_name = row[4]
        if (team_name == individual_team) and (event in LIST_OF_SCORED_RELAY_EVENTS) and ([gender, event] not in seen_relays):
            seen_relays.append([gender, event])
            selected_rows.append(row)

    for selected_row in selected_rows:
        top_relay_swims.append(selected_row)

rescored_df = top_individual_swims + top_relay_swims

## Step 3: Provide Individual Events Re-Ranking and Re-Scoring
# Sort rescored by Gender, Event, Course, and then Time
rescored_df.sort(key=lambda x: (x[0], x[1], x[2], float(timeToSec(x[5]))))  # Assuming Time is in column 5

# Add Place and Score columns
place_col_index = len(rescored_df[0])  # Next column for place
score_col_index = place_col_index + 1  # Next column for score

current_group = None
place = 0

for row in rescored_df:
    # Group by Gender, Event, Course (columns 0, 1, 2)
    gender = row[0]
    event = row[1]
    course = row[2]

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
    writer.writerow(["Gender", "Event", "Course", "Club", "Name", "Time", "AQUA", "Old Place", "Old Score", "Group", "New Place", "New Score"])  # Header
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
    gender = row[0]
    event = row[1]
    club = row[3]
    score = int(row[11])
    group = row[8]
    
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
    gender = row[0]
    event = row[1]
    course = row[2]
    club = row[3]
    score = int(row[11])
    group = row[8]
    
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
