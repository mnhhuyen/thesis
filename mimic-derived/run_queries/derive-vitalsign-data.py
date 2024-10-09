import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config_param import mimic_path, derive_path

vital_itemids = [
        223761, #temperature F
        223762, #temperature C
        220045, #heart rate,
        228151, #Aortic Pressure Signal - Diastolic
        228152, #Aortic Pressure Signal - Systolic
        220210, # respiratory rate
        224690 #respiratory rate (total)
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
    
    chartevents_path = os.path.join(mimic_path, 'icu/chartevents.csv')
    save_path = os.path.join(derive_path, 'vitalsigns.csv')
    
    filtered_chartevent_df = filter_in_chart(vital_itemids, chartevents_path)

    if filtered_chartevent_df.empty:
        print(f"No data found in chartevents.csv for the given item IDs")
    else:
        filtered_chartevent_df.to_csv(save_path, index=False)
        print(f"Filtered data saved to {save_path}")