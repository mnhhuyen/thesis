import sys
import os

# Add the parent directory of 'utils' to sys.path to make sure Python can find it
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils'))

# Import the run_query function from the run_queries.py file
from utils.run_queries import run_query

### have to run ventilator_settings and oxygen_delivery first
def run_derived_data():
    tables_to_load = [
]

    run_query('derived.db', 'ventilation.sql', 'ventilation.csv', tables_to_load)
