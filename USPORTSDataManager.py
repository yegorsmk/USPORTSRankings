### IMPORTS AND GLOBALS ###
## IMPORTS
import csv

## GLOBALS
OUTPUT_PREFIX = "OUTPUT_"
MENS_TEAM_SCORING_DB_FILENAME = OUTPUT_PREFIX + "mens_team_scoring_db.csv"
WOMENS_TEAM_SCORING_DB_FILENAME = OUTPUT_PREFIX + "womens_team_scoring_db.csv"

EVENT_SCORING_DB_FILENAME = OUTPUT_PREFIX + "event_scoring_db.csv"

RESTRICTED_EVENT_SCORING_DB_FILENAME = OUTPUT_PREFIX + "restricted_event_scoring_db.csv"

### CLASSES AND METHODS ###
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

def ProvidePowerRankings(gender, event, course):
    power_rankings_raw = []
    power_rankings_final = []

    try:
        with open(EVENT_SCORING_DB_FILENAME, mode='r') as event_file:
            csv_reader = csv.DictReader(event_file)  # Use DictReader for easier column-based filtering
            for row in csv_reader:
                # Filter rows based on the criteria
                if (row['Gender'] == gender and 
                    row['Event'] == event and 
                    row['Course'] == course):
                    power_rankings_raw.append(row)
    except FileNotFoundError:
        print(f"Error: File {EVENT_SCORING_DB_FILENAME} not found.")
    except Exception as e:
        print(f"An error occurred while reading {EVENT_SCORING_DB_FILENAME}: {e}")

    # Convert the filtered rows into a final list format (optional step for presentation)
    for row in power_rankings_raw:
        # Convert time using secToTime before appending to the final list
        time_in_sec = float(row['Time'])  # Assuming 'Time' is in seconds
        formatted_time = secToTime(time_in_sec)  # Format the time
        
        power_rankings_final.append([
            row['Place'],
            row['Name'],
            row['Team'],
            formatted_time,  # Use the formatted time string,
            row['AQUA'],
            row['Score']
        ])

    return power_rankings_final

def ProvidePsychRankings(gender, event, course):
    psych_rankings_raw = []
    psych_rankings_final = []

    try:
        with open(RESTRICTED_EVENT_SCORING_DB_FILENAME, mode='r') as event_file:
            csv_reader = csv.DictReader(event_file)  # Use DictReader for easier column-based filtering
            for row in csv_reader:
                # Filter rows based on the criteria
                if (row['Gender'] == gender and 
                    row['Event'] == event and 
                    row['Course'] == course):
                    psych_rankings_raw.append(row)
    except FileNotFoundError:
        print(f"Error: File {RESTRICTED_EVENT_SCORING_DB_FILENAME} not found.")
    except Exception as e:
        print(f"An error occurred while reading {RESTRICTED_EVENT_SCORING_DB_FILENAME}: {e}")

    # Convert the filtered rows into a final list format (optional step for presentation)
    for row in psych_rankings_raw:
        # Convert time using secToTime before appending to the final list
        time_in_sec = float(row['Time'])  # Assuming 'Time' is in seconds
        formatted_time = secToTime(time_in_sec)  # Format the time
        
        # Include the new rankings (New Place and New Score) from the restricted event scoring file
        psych_rankings_final.append([
            row['New Place'],           # Use New Place
            row['Name'],
            row['Team'],
            formatted_time,            # Use the formatted time string,
            row['AQUA'],
            row['New Score']           # Use New Score
        ])

    return psych_rankings_final

def ProvideTeamRankings():
    womens_team_rankings = []
    mens_team_rankings = []

    # Load data for women's team rankings
    try:
        with open(WOMENS_TEAM_SCORING_DB_FILENAME, mode='r') as womens_file:
            csv_reader = csv.reader(womens_file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                womens_team_rankings.append(row)
    except FileNotFoundError:
        print(f"Error: File {WOMENS_TEAM_SCORING_DB_FILENAME} not found.")
    except Exception as e:
        print(f"An error occurred while reading {WOMENS_TEAM_SCORING_DB_FILENAME}: {e}")

    # Load data for men's team rankings
    try:
        with open(MENS_TEAM_SCORING_DB_FILENAME, mode='r') as mens_file:
            csv_reader = csv.reader(mens_file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                mens_team_rankings.append(row)
    except FileNotFoundError:
        print(f"Error: File {MENS_TEAM_SCORING_DB_FILENAME} not found.")
    except Exception as e:
        print(f"An error occurred while reading {MENS_TEAM_SCORING_DB_FILENAME}: {e}")

    return womens_team_rankings, mens_team_rankings

### MAIN SECTION ###
