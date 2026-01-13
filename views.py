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

DATE_OF_LAST_UPDATE = "January 12th, 2026" 
VERSION_NUMBER = "1.05 - WEEK 5 - HAPPY NEW YEAR!"
ANALYTICS_LOG = os.path.join(app.root_path, "usage_log.csv")

USAGE_PASSWORD = "REMOVED_PASSWORD"

def usage_auth_required():
    return request.args.get("pwd", "") == USAGE_PASSWORD

def _get_client_fingerprint():
    """
    Hash of IP + User-Agent so you can estimate 'unique users'
    without storing raw IPs.
    """
    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "")
    ua = request.headers.get("User-Agent", "")
    return ip


def log_event(event_type, route, detail=""):
    ts = datetime.utcnow().isoformat()
    client_id = _get_client_fingerprint()

    row = [ts, event_type, route, client_id, request.method, detail]

    file_exists = os.path.exists(ANALYTICS_LOG)
    with open(ANALYTICS_LOG, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(
                ["timestamp", "event_type", "route", "client_id", "method", "detail"]
            )
        writer.writerow(row)


def parse_detail(detail_str: str) -> dict:
    """
    Parse the detail string like 'gender=Men,event=100m Freestyle,course=Short Course (25m)'
    into a dict: {'gender': 'Men', 'event': '100m Freestyle', 'course': 'Short Course (25m)'}
    """
    if not isinstance(detail_str, str):
        return {}
    parts = [p.strip() for p in detail_str.split(",") if p.strip()]
    out = {}
    for p in parts:
        if "=" in p:
            k, v = p.split("=", 1)
            out[k.strip()] = v.strip()
    return out


@app.route('/')
def home():
    """Renders the home page."""
    log_event("page_view", "/")
    return render_template(
        'index.html',
        title='Home',
        year=datetime.now().year,
        version=VERSION_NUMBER
    )

@app.route('/insights')
def insights():
    """Renders the insights page."""
    log_event("page_view", "/insights")
    return render_template(
        'insights.html',
        title='2025 U SPORTS Insights',
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

        # Log the query
        log_event(
            "power_query",
            "/power",
            detail=f"gender={TARGET_GENDER},event={TARGET_EVENT},course={TARGET_COURSE}"
        )

        # Call ProvideIndividualRankings to get filtered rankings
        power_rankings = USPORTSDataManager.ProvidePowerRankings(TARGET_GENDER, TARGET_EVENT, TARGET_COURSE)

        # Convert rankings to a pandas DataFrame for better presentation
        rankings_df = pd.DataFrame(power_rankings, columns=['Place', 'Name', 'Team', 'Conference', 'Time', 'AQUA', 'Score'])

        # Convert the DataFrame to HTML
        rankings_html = rankings_df.to_html(classes='table table-striped sortable', index=False)

        return render_template(
            'power.html',
            title='Unofficial U SPORTS Power Rankings as of ' + DATE_OF_LAST_UPDATE,
            year=datetime.now().year,
            message=f"{TARGET_GENDER}'s {TARGET_EVENT} {TARGET_COURSE}",
            data=rankings_html,  # Pass the table as HTML to the template
            selected_gender = TARGET_GENDER,
            selected_event = TARGET_EVENT,
            version=VERSION_NUMBER
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

        log_event(
            "psych_query",
            "/psych",
            detail=f"gender={TARGET_GENDER},event={TARGET_EVENT},course={TARGET_COURSE}"
        )

        # Call ProvideIndividualRankings to get filtered rankings
        psych_rankings = USPORTSDataManager.ProvidePsychRankings(TARGET_GENDER, TARGET_EVENT, TARGET_COURSE)

        # Convert rankings to a pandas DataFrame for better presentation
        rankings_df = pd.DataFrame(psych_rankings, columns=['Place', 'Name', 'Team', 'Conference', 'Time', 'AQUA', 'Score'])

        # Convert the DataFrame to HTML
        rankings_html = rankings_df.to_html(classes='table table-striped sortable', index=False)

        return render_template(
            'psych.html',
            title='Unofficial U SPORTS Psych Rankings as of ' + DATE_OF_LAST_UPDATE,
            year=datetime.now().year,
            message=f"{TARGET_GENDER}'s {TARGET_EVENT} {TARGET_COURSE}",
            data=rankings_html,  # Pass the table as HTML to the template
            selected_gender = TARGET_GENDER,
            selected_event = TARGET_EVENT,
            version=VERSION_NUMBER
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
    log_event("page_view", "/team")
    womens_team_rankings, mens_team_rankings = USPORTSDataManager.ProvideTeamRankings()

    # Convert to pandas DataFrame
    womens_df = pd.DataFrame(womens_team_rankings, columns=['Rank', 'Team', 'Score', 'Conference'])
    mens_df = pd.DataFrame(mens_team_rankings, columns=['Rank', 'Team', 'Score', 'Conference'])

    # Convert DataFrame to HTML
    womens_html = womens_df.to_html(classes='table table-striped sortable', index=False)
    mens_html = mens_df.to_html(classes='table table-striped sortable', index=False)

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

        log_event(
            "name_search",
            "/namesearch",
            detail=f"name={TARGET_NAME},course={TARGET_COURSE}"
        )

        # Call ProvideNameRankings to get filtered rankings
        name_results = USPORTSDataManager.ProvideNameResults(TARGET_NAME, TARGET_COURSE)

        # Convert rankings to a pandas DataFrame for better presentation
        rankings_df = pd.DataFrame(name_results, columns=['Event', 'Time', 'AQUA', 'Place', 'Score'])

        # Convert the DataFrame to HTML
        rankings_html = rankings_df.to_html(classes='table table-striped sortable', index=False)

        return render_template(
            'namesearch.html',
            title='Unofficial U SPORTS Power Rankings as of ' + DATE_OF_LAST_UPDATE,
            year=datetime.now().year,
            message=f"{TARGET_NAME}'s {TARGET_COURSE} Rankings",
            data=rankings_html,  # Pass the table as HTML to the template,
            version=VERSION_NUMBER
        )
    else:  # GET request
        return render_template(
            'namesearch.html',
            title='Unofficial U SPORTS Power Rankings as of ' + DATE_OF_LAST_UPDATE,
            year=datetime.now().year,
            version=VERSION_NUMBER,
            message='Please enter a Name, and click Get Rankings.',
            data="",
        )

@app.route('/teamsearch', methods=['GET', 'POST'])
def teamSearch():
    """Handles both rendering and form submission for the Team Search page."""
    if request.method == 'POST':
        TARGET_TEAM = request.form['TARGET_TEAM']
        TARGET_COURSE = "Short Course (25m)"

        log_event(
            "team_search",
            "/teamsearch",
            detail=f"team={TARGET_TEAM},course={TARGET_COURSE}"
        )

        # Call ProvideIndividualRankings to get filtered rankings
        team_results = USPORTSDataManager.ProvideTeamResults(TARGET_TEAM, TARGET_COURSE)

        # Convert rankings to a pandas DataFrame for better presentation
        rankings_df = pd.DataFrame(team_results, columns=['Gender', 'Event', 'Place', 'Name', 'Time', 'AQUA', 'Score'])

        # Convert the DataFrame to HTML
        rankings_html = rankings_df.to_html(classes='table table-striped sortable', index=False)

        return render_template(
            'teamsearch.html',
            title='Unofficial U SPORTS Psych Rankings as of ' + DATE_OF_LAST_UPDATE,
            year=datetime.now().year,
            message=f"{TARGET_TEAM}'s {TARGET_COURSE} Rankings",
            data=rankings_html, # Pass the table as HTML to the template
            selected_team = TARGET_TEAM,
            version=VERSION_NUMBER
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

@app.route('/usage')
def usage():
    """Usage statistics dashboard."""

    # Password protection
    if not usage_auth_required():
        return '''
            <h2>Usage Stats – Password Required</h2>
            <form method="get">
                <input type="password" name="pwd" placeholder="Enter password">
                <button type="submit">Submit</button>
            </form>
        '''
    log_event("page_view", "/usage")

    if not os.path.exists(ANALYTICS_LOG):
        flash("No usage data yet.")
        return render_template(
            'usage.html',
            title='Usage Statistics',
            year=datetime.now().year,
            version=VERSION_NUMBER,
            summary_html="No data yet.",
            routes_html="",
            daily_html="",
            power_gender_event_html="",
            power_name_html="",
            psych_gender_event_html="",
            psych_team_html="",
            pageviews_html="",
            ip_counts_html=""
        )

    df = pd.read_csv(ANALYTICS_LOG)

    # ------------------------
    # BASIC SUMMARY / ROUTES
    # ------------------------
    total_events = len(df)
    unique_users = df["client_id"].nunique()

    route_counts = (
        df.groupby("route")["event_type"]
        .count()
        .reset_index(name="hits")
        .sort_values("hits", ascending=False)
    )

    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    daily_counts = (
        df.groupby("date")["event_type"]
        .count()
        .reset_index(name="hits")
        .sort_values("date")
    )

    summary_df = pd.DataFrame(
        {
            "metric": ["Total events logged", "Unique visitors (approx)"],
            "value": [total_events, unique_users],
        }
    )

    summary_html = summary_df.to_html(classes="table table-striped", index=False)
    routes_html = route_counts.to_html(classes="table table-striped", index=False)
    daily_html = daily_counts.to_html(classes="table table-striped", index=False)

    # -----------------------------------------------------------------
    # 1) Power Rankings: most popular Gender-Event populations by access
    # -----------------------------------------------------------------
    power_df = df[df["event_type"] == "power_query"].copy()
    if not power_df.empty:
        power_details = power_df["detail"].fillna("").apply(parse_detail)
        power_df["gender"] = power_details.apply(lambda d: d.get("gender", ""))
        power_df["event"] = power_details.apply(lambda d: d.get("event", ""))

        power_gender_event_counts = (
            power_df.groupby(["gender", "event"])
            .size()
            .reset_index(name="hits")
            .sort_values("hits", ascending=False)
        )
        power_gender_event_html = power_gender_event_counts.to_html(
            classes="table table-striped", index=False
        )
    else:
        power_gender_event_html = "<p>No Power Rankings queries yet.</p>"

    # ---------------------------------------------------
    # 2) Power Rankings: most popular names by accesses
    #    (from /namesearch, event_type = 'name_search')
    # ---------------------------------------------------
    name_df = df[df["event_type"] == "name_search"].copy()
    if not name_df.empty:
        name_details = name_df["detail"].fillna("").apply(parse_detail)
        name_df["name"] = name_details.apply(lambda d: d.get("name", ""))

        power_name_counts = (
            name_df.groupby("name")
            .size()
            .reset_index(name="hits")
            .sort_values("hits", ascending=False)
        )
        power_name_html = power_name_counts.to_html(
            classes="table table-striped", index=False
        )
    else:
        power_name_html = "<p>No name searches yet.</p>"

    # -----------------------------------------------------------------
    # 3) Psych Sheets: most popular Gender-Event populations by access
    # -----------------------------------------------------------------
    psych_df = df[df["event_type"] == "psych_query"].copy()
    if not psych_df.empty:
        psych_details = psych_df["detail"].fillna("").apply(parse_detail)
        psych_df["gender"] = psych_details.apply(lambda d: d.get("gender", ""))
        psych_df["event"] = psych_details.apply(lambda d: d.get("event", ""))

        psych_gender_event_counts = (
            psych_df.groupby(["gender", "event"])
            .size()
            .reset_index(name="hits")
            .sort_values("hits", ascending=False)
        )
        psych_gender_event_html = psych_gender_event_counts.to_html(
            classes="table table-striped", index=False
        )
    else:
        psych_gender_event_html = "<p>No Psych Rankings queries yet.</p>"

    # ---------------------------------------------------------
    # 4) Psych Rankings: most popular teams (team search hits)
    # ---------------------------------------------------------
    team_search_df = df[df["event_type"] == "team_search"].copy()
    if not team_search_df.empty:
        team_details = team_search_df["detail"].fillna("").apply(parse_detail)
        team_search_df["team"] = team_details.apply(lambda d: d.get("team", ""))

        psych_team_counts = (
            team_search_df.groupby("team")
            .size()
            .reset_index(name="hits")
            .sort_values("hits", ascending=False)
        )
        psych_team_html = psych_team_counts.to_html(
            classes="table table-striped", index=False
        )
    else:
        psych_team_html = "<p>No team searches yet.</p>"

    # ---------------------------------------------------
    # 5) Team / Insights / Usage pageviews
    # ---------------------------------------------------
    pageviews = []
    for route in ["/team", "/insights", "/usage"]:
        count = df[(df["event_type"] == "page_view") & (df["route"] == route)].shape[0]
        pageviews.append({"route": route, "pageviews": count})

    pageviews_df = pd.DataFrame(pageviews)
    pageviews_html = pageviews_df.to_html(classes="table table-striped", index=False)

    # ---------------------------------------------------
    # 6) IPs and total accesses
    # ---------------------------------------------------
    ip_counts = (
        df.groupby("client_id")["event_type"]
        .count()
        .reset_index(name="hits")
        .sort_values("hits", ascending=False)
    )
    ip_counts_html = ip_counts.to_html(classes="table table-striped", index=False)

    # NOTE: For geographic location ("where they're from"), you'd need to
    # run these IPs through a GeoIP service or database (e.g., ipinfo,
    # MaxMind GeoLite2, etc.). That's external to this app and usually
    # requires an API key or local DB, so here we just list the IPs +
    # hit counts.

    # ---------------------------------------------------
    # 7) Full raw log dump as a table
    # ---------------------------------------------------
    full_log_html = df.to_html(classes="table table-striped", index=False)


    return render_template(
        'usage.html',
        title='Usage Statistics',
        year=datetime.now().year,
        version=VERSION_NUMBER,
        summary_html=summary_html,
        routes_html=routes_html,
        daily_html=daily_html,
        power_gender_event_html=power_gender_event_html,
        power_name_html=power_name_html,
        psych_gender_event_html=psych_gender_event_html,
        psych_team_html=psych_team_html,
        pageviews_html=pageviews_html,
        ip_counts_html=ip_counts_html,
        full_log_html=full_log_html,  # NEW
    )

from flask import send_file  # you already have send_from_directory, this is separate

@app.route('/usage_log_download')
def usage_log_download():
    # Reuse password protection
    if not usage_auth_required():
        return redirect(url_for('usage'))

    if not os.path.exists(ANALYTICS_LOG):
        flash("No usage log file to download yet.")
        # preserve pwd param if present
        return redirect(url_for('usage', pwd=request.args.get('pwd', '')))

    return send_file(
        ANALYTICS_LOG,
        as_attachment=True,
        download_name="usage_log.csv"  # Flask >= 2.0; drop this arg if you're on older Flask
    )

