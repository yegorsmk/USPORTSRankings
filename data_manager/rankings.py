"""
Power, Psych, and Team rankings pages.
"""

import csv

from shared.config import (
    EVENT_SCORING_DB_FILENAME, RESTRICTED_EVENT_SCORING_DB_FILENAME,
    MENS_TEAM_SCORING_DB_FILENAME, WOMENS_TEAM_SCORING_DB_FILENAME,
)
from shared.times import secToTime

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
            row['Conference'],
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
            row['Conference'],
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
