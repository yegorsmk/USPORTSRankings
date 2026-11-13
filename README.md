# BBRankings: Unofficial U SPORTS Swimming Rankings

BBRankings predicts how the U SPORTS swimming championships would score if they were held today. It takes every varsity swimmer's best short course (25m) times of the season, ranks each event, awards championship points by place, and adds those points up into team scores.

The project has two parts:

| Part | What it does | Where it runs |
|---|---|---|
| **Merger** | Reads Swimrankings Excel exports and writes the rankings as `OUTPUT_*.csv` files | Locally, on your machine, once per update |
| **Website** | A Flask site that reads the `OUTPUT_*.csv` files and shows the rankings | Azure App Service (and locally for testing) |

The website never scrapes (though it used to before Swimrankings.ca implemented their anti-botting system) or computes anything heavy. It only filters the CSVs the merger produced.

---

## Contents

- [Quick start](#quick-start)
- [Updating the rankings](#updating-the-rankings)
- [How scoring works](#how-scoring-works)
- [Website pages](#website-pages)
- [Project layout](#project-layout)
- [Input files](#input-files)
- [Output files](#output-files)
- [Manual results and the watchlist](#manual-results-and-the-watchlist)
- [Deploying to Azure](#deploying-to-azure)
- [History](#history)

---

## Quick start

Requires **Python 3.13**. Run everything from the project root.

```bash
python3 -m venv .venv
source .venv/bin/activate              # Windows: .venv\Scripts\activate
pip install -r requirements.txt        # website + merger packages
```

Then:

```bash
python run_merger.py   # build the OUTPUT_*.csv files from INPUT/
python runserver.py    # start the website at http://localhost:5555
```

### Which requirements file?

| File | Contains | Used by |
|---|---|---|
| `requirements.txt` | Flask, pandas, numpy, python-dotenv, gunicorn | The website. Azure installs this on every deploy, so keep it small. |
| `requirements-scraper.txt` | Everything above, plus openpyxl (reading Excel), requests, beautifulsoup4, playwright | Local work: the merger and the old scraper |

---

## Updating the rankings

This is the routine for each weekly (or so) update.

1. **Download the Swimrankings exports** into `INPUT/`, replacing last week's files. See [Input files](#input-files) for the exact names.
2. **Check the watchlist.** Open `OUTPUT_watchlist.csv` from the last run and look up those swimmers' Swimrankings profiles for swims at foreign clubs. Type any faster times into `INPUT/manual_results.xlsx`. See [Manual results and the watchlist](#manual-results-and-the-watchlist).
3. **Run the merger:**
   ```bash
   python run_merger.py
   ```
   It prints `Done Step N/10` as it goes, then the watchlist. Read any `⚠️` lines: they mean a file or a manual row was skipped.
4. **Update the date and version** at the top of `views.py`:
   ```python
   DATE_OF_LAST_UPDATE = "October 30, 2026"
   VERSION_NUMBER = "3.1 - WEEK 1"
   ```
5. **Check the site locally** with `python runserver.py`.
6. **Archive this report** by copying `INPUT/` and the `OUTPUT_*` files into a dated folder, e.g. `2026-2027 Season/Nov 8th Report/`. Past seasons live in `Archive/`.
7. **Deploy** from VS Code.

---

## How scoring works

### 1. Collecting each swimmer's best times

- **Varsity swims:** every swim from each team's Swimrankings export. A swimmer is identified by **name + birthdate** (e.g. `FEDDAG, Hocine_2004-06-16 00:00:00`), because exports don't include a Swimrankings ID.
- **Club swims:** swimmers often race for their home club (e.g. a McGill swimmer racing for CAMO). The Canada-wide 17+ export is filtered down to known varsity swimmers. A club swim is used if it's faster, or if it's an event they haven't swum for their university, and **it's always credited to their university**.
- **Manual swims:** times typed into `INPUT/manual_results.xlsx`, for swims the exports can't provide (see below). Again, the fastest time wins.

Only scoring events count, and lap/split sheets in the exports are ignored. A swimmer only counts as varsity once they have **at least one swim for their university** this season.

### 2. Power Rankings (unrestricted)

Every swim is ranked within its gender and event, and places 1–24 earn points:

| Place | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Points | 32 | 28 | 27 | 26 | 25 | 24 | 23 | 22 | 20 | 17 | 16 | 15 | 14 | 13 | 12 | 11 | 9 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |

This ignores entry limits, so one swimmer can score in many events.

### 3. Psych Rankings (restricted)

This applies the championship entry limits, then re-ranks and re-scores:

- **4 individual events per swimmer:** their 4 highest-scoring swims (ties broken by AQUA points, then time).
- **1 relay per team** per gender and relay event: the team's fastest.

### 4. Team Scores

Each team's Psych Ranking points added up, for men, women and combined.

Point tables, relay multipliers and limits are in [merger/scoring_rules.py](merger/scoring_rules.py).

---

## Website pages

| URL | Menu | Shows | Data file |
|---|---|---|---|
| `/` | Home | Landing page | – |
| `/power` | Power Rankings → By Event | Every ranked swim for one gender + event | `OUTPUT_event_scoring_db.csv` |
| `/namesearch` | Power Rankings → By Name | A swimmer's events and points, plus a total. Search ignores capitals, commas and word order, and partial names work. | `OUTPUT_event_scoring_db.csv` |
| `/psych` | Psych Sheets → By Event | Restricted rankings for one gender + event | `OUTPUT_restricted_event_scoring_db.csv` |
| `/teamsearch` | Psych Sheets → By Team | All of one team's scoring swims | `OUTPUT_restricted_event_scoring_db.csv` |
| `/team` | Team Scores | Men's and women's team standings | `OUTPUT_mens/womens_team_scoring_db.csv` |
| `/usage` | *(hidden)* | Visitor statistics. Needs `?pwd=<USAGE_PASSWORD>`. | `usage_log.csv` |
| `/usage_log_download` | *(hidden)* | Downloads the raw usage log (same password) | `usage_log.csv` |

Every page view and search is appended to `FlaskTest/usage_log.csv` (timestamp, page, visitor IP, search details). If `USAGE_PASSWORD` isn't set, the two usage pages stay locked for everyone. The rest of the site works normally.

Team codes are shown as short university names on the Team Scores page through `TEAM_FULL_NAMES` in [views.py](views.py).

---

## Project layout

```
├── run_merger.py            # Entry point: build the rankings
├── runserver.py             # Entry point: website (gunicorn on Azure, Flask dev server locally)
├── views.py                 # Website routes, usage logging, update date/version
│
├── merger/                  # Builds the OUTPUT_ files. The website never imports this.
│   ├── pipeline.py          #   Runs every step in order. Start reading here.
│   ├── varsity_results.py   #   Step 1–2: team exports → OUTPUT_results_db.csv
│   ├── club_results.py      #   Step 2.5: Canada 17+ export → club swims of varsity swimmers
│   ├── combine.py           #   Step 2.75–2.8: merge varsity + club + manual, fastest wins
│   ├── manual_results.py    #   Reads INPUT/manual_results.xlsx
│   ├── event_scoring.py     #   Steps 3–4: rank, score, apply entry limits, re-score
│   ├── team_scoring.py      #   Steps 5–10: team totals and per-event breakdown
│   ├── scoring_rules.py     #   Points per place, relay multipliers, limits
│   ├── watchlist.py         #   Step 11: international swimmers to check by hand
│   └── progress_tracker.py
│
├── data_manager/            # Reads the OUTPUT_ files for the website
│   ├── rankings.py          #   Power, Psych and Team rankings
│   └── search.py            #   Name and team search
│
├── shared/                  # Used by both the merger and the website
│   ├── config.py            #   Run mode, season year, every input/output filename
│   ├── teams.py             #   Conferences and Swimrankings club codes
│   ├── events.py            #   Genders, event names, courses
│   └── times.py             #   Swim time ↔ seconds
│
├── FlaskTest/               # Flask app package: templates/ and static/ (Bootstrap, jQuery, sorttable.js)
├── INPUT/                   # Swimrankings exports + manual_results.xlsx (gitignored)
├── OUTPUT_*.csv             # Merger output (gitignored)
├── 2026-2027 Season/        # This season's archived reports
├── Archive/                 # Past seasons' reports and old code
├── OLDUSPORTSDataGrabber.py # Old scraper, obsolete since Feb 2026 (see History)
├── requirements.txt         # Website packages (deployed)
├── requirements-scraper.txt # Local packages
├── runtime.txt              # Python version note (Azure ignores it; see Deploying)
└── .deployment              # Tells Azure to pip install on deploy
```

---

## Input files

All of these go in `INPUT/`. `2026` is `USPORTS_YEAR` in [shared/config.py](shared/config.py). If the year in the filenames Swimrankings gives you changes, update `USPORTS_YEAR` to match, or the merger won't find the files.

| File | What it is |
|---|---|
| `CAN-<CLUB>_2026_SCM_Men.xlsx`, `CAN-<CLUB>_2026_SCM_Women.xlsx` | One pair per university, e.g. `CAN-MCGILL_2026_SCM_Men.xlsx`. `<CLUB>` must be a code in `SWIMRANKINGS_CLUB_TO_TEAM` in [shared/teams.py](shared/teams.py), or the file is skipped. |
| `CAN_2026_SCM_Men_17-99.xlsx`, `CAN_2026_SCM_Women_17-99.xlsx` | Canada-wide results for ages 17+. Used to find varsity swimmers' club swims, including swims abroad for a Canadian club. |
| `manual_results.xlsx` | Hand-entered swims (optional). |

The exports use one sheet per event (`50m Fr`, `100m Bk`, …) with a header on row 2. The merger reads the `FULLNAME`, `BIRTHDATE`, `NATION`, `CLUBCODE`, `SWIMTIME_N` and `PTS_FINA` columns.

These files contain athlete names and birthdates, which is why `*.xlsx` and `*.csv` are gitignored.

---

## Output files

| File | Contents | Read by website |
|---|---|---|
| `OUTPUT_results_db.csv` | Varsity swims from team exports | |
| `OUTPUT_athlete_ids.csv` | Varsity swimmer IDs and their university | |
| `OUTPUT_club_results_db.csv` | Varsity swimmers' best club swims | |
| `OUTPUT_combined_results_db.csv` | Varsity + club + manual, best time per event | |
| `OUTPUT_event_scoring_db.csv` | Power Rankings: every swim ranked and scored | ✅ |
| `OUTPUT_restricted_event_scoring_db.csv` | Psych Rankings: after entry limits | ✅ |
| `OUTPUT_mens_team_scoring_db.csv`, `OUTPUT_womens_team_scoring_db.csv` | Team standings | ✅ |
| `OUTPUT_team_scoring_db.csv` | Combined team standings | |
| `OUTPUT_team_breakdown_db.csv` | Each team's points per event | |
| `OUTPUT_watchlist.csv` | Swimmers to check by hand | |
| `OUTPUT_progress_tracker.txt` | Teams processed in the last run | |

All times are stored in **seconds** (e.g. `109.37`). The website formats them as `1:49.37`.

---

## Manual results and the watchlist

Swimrankings blocks reports for most other countries. A swim at a **foreign club**, such as a French student at the French championships, never shows up in the exports.

### The watchlist

At the end of every run the merger prints, and saves to `OUTPUT_watchlist.csv`, every **non-Canadian swimmer who placed top 24 last season**. It includes their birthdate, team, last season's events and places, and whether they've swum for their university yet this season. Look them up on Swimrankings by hand. Profile pages show swims from every country, even though reports don't.

Canadians aren't listed because their swims for Canadian clubs, including abroad, are already in the 17+ export.

Settings in [shared/config.py](shared/config.py):
- `PREVIOUS_SEASON_REPORT_FOLDER`: last season's final report, which provides the top-24 list
- `WATCHLIST_PLACE_CUTOFF` in [merger/watchlist.py](merger/watchlist.py): defaults to 24

The watchlist can't catch **first-year international swimmers**, since they have no previous season. Keep an eye on new recruits.

## Deploying to Azure

The site runs on **Azure App Service** (Linux, Python 3.13, app `bbrankings`), currently on the **Free (F1)** plan.

## History

- **2024–25:** `Archive/2024-2025 Season/`. The original version scraped Swimrankings directly: athlete names came from official rosters, then each athlete's profile was scraped for season bests.
- **Feb 23rd, 2026:** Swimrankings added anti-bot protection and started blocking the scraper. `OLDUSPORTSDataGrabber.py` is kept for reference but no longer works.
- **Feb 24th, 2026:** the scraper was replaced by the **merge method**, which builds rankings from Excel exports downloaded by hand. The Canada 17+ export picks up club swims.
- **Nov 2026:**
  - Hosted on Azure.
  - Name search fixed.
  - Manual results and the watchlist added for swims at foreign clubs.
  - The two large scripts (`NEWUSPORTSDataMerger.py`, `USPORTSDataManager.py`) split into the `merger/`, `data_manager/` and `shared/` packages.
