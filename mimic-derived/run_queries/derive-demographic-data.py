import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config_param import mimic_path, derive_path
# Function to load event item IDs from d_items.csv
def load_ids(item_event_path, chunksize=10**6):
    chunk_list = []
    for chunk in pd.read_csv(item_event_path, chunksize=chunksize):
        chunk_list.append(chunk)
    return pd.concat(chunk_list)

# Function to filter item IDs based on keyword (e.g., height, weight)
def filter_by_keyword(keyword, event_df):
    found_df = event_df[event_df['label'].str.contains(keyword, case=False)]
    item_found = found_df['itemid'].unique()
    return item_found

# Function to filter the chartevents.csv file based on item IDs
def filter_in_chart(item_ids, chartevents_path, chunksize=10**6):
    chartevents_df = pd.read_csv(chartevents_path, chunksize=chunksize)
    filtered_chartevents_list = []

    for chunk in chartevents_df:
        filtered_chunk = chunk[chunk['itemid'].isin(item_ids)]
        if not filtered_chunk.empty:
            filtered_chartevents_list.append(filtered_chunk)

    if filtered_chartevents_list:
        return pd.concat(filtered_chartevents_list, axis=0)
    else:
        return pd.DataFrame()  # Return empty DataFrame if nothing found

# Main function to process the MIMIC data based on a keyword and save to CSV
def mimic_derived_by_keyword(keyword, item_event_path, chartevents_path, save_path):
    # Load the event items from d_items.csv
    events_df = load_ids(item_event_path)

    # Filter item IDs by the specified keyword
    item_ids = filter_by_keyword(keyword, events_df)

    if len(item_ids) == 0:
        print(f"No item IDs found for keyword: {keyword}")
        return

    # Filter chartevents.csv based on the found item IDs
    filtered_chartevent_df = filter_in_chart(item_ids, chartevents_path)

    if filtered_chartevent_df.empty:
        print(f"No data found in chartevents.csv for keyword: {keyword}")
    else:
        # Save the filtered result to a CSV file
        filtered_chartevent_df.to_csv(save_path, index=False)
        print(f"Data for {keyword} saved to {save_path}")


if __name__ == "__main__":
    keyword = sys.argv[1]
    file_event_path = os.path.join(mimic_path, 'icu/d_items.csv')
    chartevents_path = os.path.join(mimic_path, 'icu/chartevents.csv')
    save_path = os.path.join(derive_path, '{keyword}.csv')

    mimic_derived_by_keyword(keyword, file_event_path, chartevents_path, save_path)
