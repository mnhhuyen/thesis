import pandas as pd
import os
from config.config_param import target_patients_path  # Assuming mimic_path is not needed here

# Define file paths
file_path = '/media/data/huyennm/mimic-iv/notebook/demographics/demographics_results/race_output.csv'
sorted_path = '/media/data/huyennm/mimic-iv/notebook/demographics/demographics_runs/sorted.csv'

# Load the target patients data
target_patients = pd.read_csv(target_patients_path)

# Function to sort patient data
def sort_patient_data(file_path):
    df = pd.read_csv(file_path)  # Read the input CSV file
    df = df.set_index('stay_id').reindex(target_patients['stay_id']).reset_index()  # Reindex based on target_patients
    return df

# Function to reindex and save the sorted data
def reindex(file_path, sorted_path):
    sorted_data = sort_patient_data(file_path)  # Sort the patient data
    sorted_data.to_csv(sorted_path, index=False)  # Save sorted data to the specified path

if __name__ == "__main__":
    reindex(file_path, sorted_path)  # Call the reindex function with input and output paths
