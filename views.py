"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import flash
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import redirect
from flask import url_for
from FlaskTest import app
import os
import pandas as pd
import numpy as np
import hashlib
import signal
import csv

import USPORTSDataManager

from datetime import date

DATE_OF_LAST_UPDATE = "December 10th, 2024" 
VERSION_NUMBER = "2.30"

@app.route('/')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home',
        year=datetime.now().year,
        version=VERSION_NUMBER
    )

@app.route('/power', methods=['GET', 'POST'])
def power():
    """Handles both rendering and form submission for the Individual Rankings page."""
    if request.method == 'POST':
        TARGET_GENDER = request.form['TARGET_GENDER']
        TARGET_EVENT = request.form['TARGET_EVENT']
        TARGET_COURSE = "Short Course (25m)"

        # Call ProvideIndividualRankings to get filtered rankings
        power_rankings = USPORTSDataManager.ProvidePowerRankings(TARGET_GENDER, TARGET_EVENT, TARGET_COURSE)

        # Convert rankings to a pandas DataFrame for better presentation
        rankings_df = pd.DataFrame(power_rankings, columns=['Place', 'Name', 'Team', 'Time', 'AQUA', 'Score'])

        # Convert the DataFrame to HTML
        rankings_html = rankings_df.to_html(classes='table table-striped', index=False)

        return render_template(
            'power.html',
            title='Unofficial U SPORTS Power Rankings as of ' + DATE_OF_LAST_UPDATE,
            year=datetime.now().year,
            message=f"{TARGET_GENDER}'s {TARGET_EVENT} {TARGET_COURSE}",
            data=rankings_html,  # Pass the table as HTML to the template
            selected_gender = TARGET_GENDER,
            selected_event = TARGET_EVENT
        )
    else:  # GET request
        return render_template(
            'power.html',
            title='Unofficial U SPORTS Power Rankings as of ' + DATE_OF_LAST_UPDATE,
            year=datetime.now().year,
            version=VERSION_NUMBER,
            message='Please select a Gender, Event, and click Get Rankings.',
            data=""
        )

@app.route('/psych', methods=['GET', 'POST'])
def psych():
    """Handles both rendering and form submission for the Psych Rankings page."""
    if request.method == 'POST':
        TARGET_GENDER = request.form['TARGET_GENDER']
        TARGET_EVENT = request.form['TARGET_EVENT']

        if TARGET_EVENT == "Distance":
            if TARGET_GENDER == "Men":
                TARGET_EVENT = "1500m Freestyle"
            elif TARGET_GENDER == "Women":
                TARGET_EVENT = "800m Freestyle"
                
        TARGET_COURSE = "Short Course (25m)"

        # Call ProvideIndividualRankings to get filtered rankings
        psych_rankings = USPORTSDataManager.ProvidePsychRankings(TARGET_GENDER, TARGET_EVENT, TARGET_COURSE)

        # Convert rankings to a pandas DataFrame for better presentation
        rankings_df = pd.DataFrame(psych_rankings, columns=['Place', 'Name', 'Team', 'Time', 'AQUA', 'Score'])

        # Convert the DataFrame to HTML
        rankings_html = rankings_df.to_html(classes='table table-striped', index=False)

        return render_template(
            'psych.html',
            title='Unofficial U SPORTS Psych Rankings as of ' + DATE_OF_LAST_UPDATE,
            year=datetime.now().year,
            message=f"{TARGET_GENDER}'s {TARGET_EVENT} {TARGET_COURSE}",
            data=rankings_html,  # Pass the table as HTML to the template
            selected_gender = TARGET_GENDER,
            selected_event = TARGET_EVENT
        )
    else:  # GET request
        return render_template(
            'psych.html',
            title='Unofficial U SPORTS Psych Rankings as of ' + DATE_OF_LAST_UPDATE,
            year=datetime.now().year,
            version=VERSION_NUMBER,
            message='Please select a Gender, Event, and click Get Rankings.',
            data=""
        )

@app.route('/team')
def team():
    """Renders the Team Rankings report."""
    womens_team_rankings, mens_team_rankings = USPORTSDataManager.ProvideTeamRankings()

    # Convert to pandas DataFrame
    womens_df = pd.DataFrame(womens_team_rankings, columns=['Rank', 'Team', 'Score'])
    mens_df = pd.DataFrame(mens_team_rankings, columns=['Rank', 'Team', 'Score'])

    # Convert DataFrame to HTML
    womens_html = womens_df.to_html(classes='table table-striped', index=False)
    mens_html = mens_df.to_html(classes='table table-striped', index=False)

    return render_template(
        'team.html',
        title='Unofficial U SPORTS Team Rankings as of ' + DATE_OF_LAST_UPDATE,
        year=datetime.now().year,
        version=VERSION_NUMBER,
        womens_team_table=womens_html,
        mens_team_table=mens_html
    )

@app.route('/namesearch', methods=['GET', 'POST'])
def nameSearch():
    """Handles both rendering and form submission for the Name Search page."""
    if request.method == 'POST':
        TARGET_NAME = request.form['TARGET_NAME']
        TARGET_COURSE = "Short Course (25m)"

        # Call ProvideNameRankings to get filtered rankings
        name_results = USPORTSDataManager.ProvideNameResults(TARGET_NAME, TARGET_COURSE)

        # Convert rankings to a pandas DataFrame for better presentation
        rankings_df = pd.DataFrame(name_results, columns=['Event', 'Time', 'AQUA', 'Place', 'Score'])

        # Convert the DataFrame to HTML
        rankings_html = rankings_df.to_html(classes='table table-striped', index=False)

        return render_template(
            'namesearch.html',
            title='Unofficial U SPORTS Power Rankings as of ' + DATE_OF_LAST_UPDATE,
            year=datetime.now().year,
            message=f"{TARGET_NAME}'s {TARGET_COURSE} Rankings",
            data=rankings_html  # Pass the table as HTML to the template
        )
    else:  # GET request
        return render_template(
            'namesearch.html',
            title='Unofficial U SPORTS Power Rankings as of ' + DATE_OF_LAST_UPDATE,
            year=datetime.now().year,
            version=VERSION_NUMBER,
            message='Please enter a Name, and click Get Rankings.',
            data=""
        )

@app.route('/teamsearch', methods=['GET', 'POST'])
def teamSearch():
    """Handles both rendering and form submission for the Team Search page."""
    if request.method == 'POST':
        TARGET_TEAM = request.form['TARGET_TEAM']
        TARGET_COURSE = "Short Course (25m)"

        # Call ProvideIndividualRankings to get filtered rankings
        team_results = USPORTSDataManager.ProvideTeamResults(TARGET_TEAM, TARGET_COURSE)

        # Convert rankings to a pandas DataFrame for better presentation
        rankings_df = pd.DataFrame(team_results, columns=['Gender', 'Event', 'Place', 'Name', 'Time', 'AQUA', 'Score'])

        # Convert the DataFrame to HTML
        rankings_html = rankings_df.to_html(classes='table table-striped', index=False)

        return render_template(
            'teamsearch.html',
            title='Unofficial U SPORTS Psych Rankings as of ' + DATE_OF_LAST_UPDATE,
            year=datetime.now().year,
            message=f"{TARGET_TEAM}'s {TARGET_COURSE} Rankings",
            data=rankings_html, # Pass the table as HTML to the template
            selected_team = TARGET_TEAM
        )
    else:  # GET request
        return render_template(
            'teamsearch.html',
            title='Unofficial U SPORTS Psych Rankings as of ' + DATE_OF_LAST_UPDATE,
            year=datetime.now().year,
            version=VERSION_NUMBER,
            message='Please select a Team, and click Get Rankings.',
            data=""
        )