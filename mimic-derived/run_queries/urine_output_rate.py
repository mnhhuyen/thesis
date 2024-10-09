import sys
import os

# Add the parent directory of 'utils' to sys.path to make sure Python can find it
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils'))

# Import the run_query function from the run_queries.py file
from utils.run_queries import run_query

### have to run urine_output, weight_durations first
def run_derived_data():
    tables_to_load = [
        ('outputevents', 'icu/outputevents.csv'),
        ('icustays', 'icu/icustays.csv')
    ]

    run_query('derived.db', 'urine_output_rate.sql', 'urine_output_rate.csv', tables_to_load)
