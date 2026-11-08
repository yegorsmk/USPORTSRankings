"""
Teams, conferences, and Swimrankings club codes for the current RUN_MODE.
"""

from shared.config import RUN_MODE, RUN_MODE_USPORTS, RUN_MODE_CANADA_WEST, RUN_MODE_MCGILL

## CONFERENCES
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
        "University of British Columbia"    # NOTE: missing comma joins this name with the next one
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

TEAMS_TO_CONFERENCES = {}   # Not currently used
for conference in DICT_OF_TEAMS_BY_CONFERENCE:
    for team in DICT_OF_TEAMS_BY_CONFERENCE[conference]:
        TEAMS_TO_CONFERENCES[team] = conference

CONFERENCES = DICT_OF_TEAMS_BY_CONFERENCE.keys()   # Not currently used

## SWIMRANKINGS CLUB CODES
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

USPORTS_TEAMS = TEAM_TO_SWIMRANKINGS_CLUB.keys()   # Not currently used
