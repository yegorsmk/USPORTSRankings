"""
Name search and Team search pages.
"""

import csv

from shared.config import EVENT_SCORING_DB_FILENAME, RESTRICTED_EVENT_SCORING_DB_FILENAME
from shared.times import secToTime

def normalizeName(name):
    """
    Lowercases a name and strips commas so "SANCHEZ, Kayla", "sanchez kayla"
    and "Kayla Sanchez" all reduce to comparable words.
    :param name: str - Swimmer name in any format
    :return: list - Lowercase name words
    """
    return name.replace(',', ' ').lower().split()

def ProvideNameResults(name, course):
    name_results_raw = []
    name_results_final = []

    # Every word typed must appear in the swimmer's name, in any order, so partial names work
    search_words = normalizeName(name)
    if not search_words:
        return name_results_final

    try:
        with open(EVENT_SCORING_DB_FILENAME, mode='r') as event_file:
            csv_reader = csv.DictReader(event_file)  # Use DictReader for easier column-based filtering
            for row in csv_reader:
                # Relay rows use the team name as the swimmer name, so skip them
                if row['Event'].startswith('4 x'):
                    continue
                name_words = normalizeName(row['Name'])
                if (all(any(word in name_word for name_word in name_words) for word in search_words) and
                    row['Course'] == course):
                    name_results_raw.append(row)
    except FileNotFoundError:
        print(f"Error: File {EVENT_SCORING_DB_FILENAME} not found.")
    except Exception as e:
        print(f"An error occurred while reading {EVENT_SCORING_DB_FILENAME}: {e}")

    # Convert the filtered rows into a final list format (optional step for presentation)
    for row in name_results_raw:
        # Convert time using secToTime before appending to the final list
        time_in_sec = float(row['Time'])  # Assuming 'Time' is in seconds
        formatted_time = secToTime(time_in_sec)  # Format the time

        name_results_final.append([
            row['Name'],
            row['Team'],
            row['Event'],
            formatted_time,            # Use the formatted time string
            row['AQUA'],
            int(row['Place']),
            int(row['Score'])
        ])

    # Group each swimmer's events together, highest scoring event first
    name_results_final.sort(key=lambda x: (x[0], -x[6], x[5]))
    return name_results_final

def ProvideTeamResults(team, course):
    team_results_raw = []
    team_results_final = []

    try:
        with open(RESTRICTED_EVENT_SCORING_DB_FILENAME, mode='r') as event_file:
            csv_reader = csv.DictReader(event_file)  # Use DictReader for easier column-based filtering
            for row in csv_reader:
                # Filter rows based on the criteria
                if (row['Team'] == team and
                    row['Course'] == course):
                    team_results_raw.append(row)
    except FileNotFoundError:
        print(f"Error: File {RESTRICTED_EVENT_SCORING_DB_FILENAME} not found.")
    except Exception as e:
        print(f"An error occurred while reading {RESTRICTED_EVENT_SCORING_DB_FILENAME}: {e}")

    # Convert the filtered rows into a final list format (optional step for presentation)
    for row in team_results_raw:
        # Convert time using secToTime before appending to the final list
        time_in_sec = float(row['Time'])  # Assuming 'Time' is in seconds
        formatted_time = secToTime(time_in_sec)  # Format the time

        # Include the new rankings (New Place and New Score) from the restricted event scoring file
        team_results_final.append([
            row['Gender'],
            row['Event'],
            row['New Place'],           # Use New Place
            row['Name'],
            formatted_time,            # Use the formatted time string
            row['AQUA'],
            row['New Score']           # Use New Score
        ])

    # Sort team_results_final by the Name column (index 3)
    team_results_final.sort(key=lambda x: x[3])  # Sort by swimmer's name

    return team_results_final
