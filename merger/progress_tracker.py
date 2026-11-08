"""
Text files that record which teams (or athletes) have been processed.
Only save_to_progress_tracker is currently used.
"""

def load_progress_tracker(filename):
    try:
        with open(filename, "r") as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()

def save_to_progress_tracker(filename, club_name):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(club_name + "\n")

def load_club_progress_tracker(filename):
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

def save_to_club_progress_tracker(filename, athlete_id):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(athlete_id + "\n")
