import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config_param import mimic_path, derive_path

# Define the list of relevant itemids for mechanical ventilation
vent_itemids = [
    720, 223849, 223848, 445, 448, 449, 450, 1340, 1486, 1600, 224687,
    639, 654, 681, 682, 683, 684, 224685, 224684, 224686,
    218, 436, 535, 444, 224697, 224695, 224696, 224746, 224747,
    221, 1, 1211, 1655, 2000, 226873, 224738, 224419, 224750, 227187,
    543, 5865, 5866, 224707, 224709, 224705, 224706, 60, 437, 505, 506,
    686, 220339, 224700, 3459, 501, 502, 503, 224702, 223, 667, 668, 
    669, 670, 671, 672, 224701, 640, 227194, 225468, 225477, 467, 468, 469,
    470, 471, 227287, 226732, 223834
]

def filter_in_chart(item_ids, chartevents_path, chunksize=10**6):
    """
    Function to filter relevant rows from chartevents.csv based on the provided item IDs.
    It processes the file in chunks to handle large datasets efficiently.

    Parameters:
    - item_ids: List of item IDs to filter by
    - chartevents_path: Path to the chartevents.csv file
    - chunksize: The number of rows to read in each chunk (default is 1,000,000)

    Returns:
    - DataFrame: A DataFrame containing the filtered rows
    """
    filtered_chartevents_list = []
    
    # Read the CSV file in chunks to handle large files
    chartevents_df = pd.read_csv(chartevents_path, chunksize=chunksize)
   
    for chunk in chartevents_df:
        filtered_chunk = chunk[chunk['itemid'].isin(item_ids)]
        if not filtered_chunk.empty:
            filtered_chartevents_list.append(filtered_chunk)
    
    if filtered_chartevents_list:
        return pd.concat(filtered_chartevents_list, axis=0)
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    
    # Set up the paths using the config values from config_param.py
    chartevents_path = os.path.join(mimic_path, 'icu/chartevents.csv')
    save_path = os.path.join(derive_path, 'duration_mv.csv')
    
    # Filter the chartevents data based on item IDs
    filtered_chartevent_df = filter_in_chart(vent_itemids, chartevents_path)
    
    # Check if the filtered DataFrame is empty
    if filtered_chartevent_df.empty:
        print(f"No data found in chartevents.csv for the given item IDs")
    else:
        # Save the filtered result to a CSV file
        filtered_chartevent_df.to_csv(save_path, index=False)
        print(f"Filtered data saved to {save_path}")
