import sys
import os

# Add the parent directory of 'utils' to sys.path to make sure Python can find it
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils'))

# Import the run_query function from the run_queries.py file
from utils.run_queries import run_query

def run_derived_data():
    tables_to_load = [
        ('chartevents', 'icu/chartevents.csv'),
        ('labevents', 'hosp/labevents.csv')
    ]

    run_query('derived.db', 'cardiac_marker.sql', 'cardiac_marker.csv', tables_to_load)
