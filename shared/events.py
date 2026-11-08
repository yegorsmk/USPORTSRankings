"""
Genders, event names, and pool courses.
"""

## GENDERS
GENDER_MEN = "Men"
GENDER_WOMEN = "Women"
GENDERS = ["Men", "Women"]

GENDER_MEN_INT = "1"
GENDER_WOMEN_INT = "2"
GENDER_INTS = [GENDER_MEN_INT, GENDER_WOMEN_INT]   # Not currently used

## EVENTS
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

# Not currently used
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

# Swimrankings sheet names → event names
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

## COURSES
COURSE_SCM = "Short Course (25m)"
COURSE_LCM = "Long Course (50m)"   # Not currently used
