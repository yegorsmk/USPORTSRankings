"# SwimScout" 

## Running

Run everything from the project root.

- **Update the rankings:** put the Swimrankings exports in `INPUT/`, then run `python run_merger.py`. This writes the `OUTPUT_*` files.
- **Run the website locally:** `python runserver.py`, then open http://localhost:5555

## Code layout

- `shared/`: used by both the merger and the website
  - `config.py`: run mode, season year, and every input and output filename
  - `teams.py`: conferences and Swimrankings club codes
  - `events.py`: genders, event names, courses
  - `times.py`: converting swim times to and from seconds
- `merger/`: builds the `OUTPUT_*` files (the website never imports it). Start with `pipeline.py`, which runs the steps in order.
- `data_manager/`: reads the `OUTPUT_*` files for the website
  - `rankings.py`: Power, Psych, and Team rankings
  - `search.py`: name and team search
- `views.py`: the website's pages
- `FlaskTest/`: the Flask app, templates, and static files
