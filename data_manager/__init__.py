"""
Reads the OUTPUT_ files for the website.
views.py calls these as data_manager.ProvidePowerRankings(...) and so on.
"""

from data_manager.rankings import ProvidePowerRankings, ProvidePsychRankings, ProvideTeamRankings
from data_manager.search import normalizeName, ProvideNameResults, ProvideTeamResults
