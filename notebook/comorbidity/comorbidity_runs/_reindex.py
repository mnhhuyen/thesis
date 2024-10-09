import pandas as pd
import os
from config.config_param import target_patients_path

file_path = '/media/data/huyennm/mimic-iv/notebook/comorbidity/comorbidity_results/patients_with_comorbidity.csv'
sorted_path = '/media/data/huyennm/mimic-iv/notebook/comorbidity/comorbidity_runs/sorted.csv'

target_patients = pd.read_csv(target_patients_path)

def sort_patient_data(file_path):
    df = pd.read_csv(file_path)
    df = df.set_index('stay_id')
    
    # Convert 'stay_id' column to Index and find missing indices
    target_index = pd.Index(target_patients['stay_id'])
    missing_indices = target_index.difference(df.index)

    if not missing_indices.empty:
        raise ValueError("Missing indices in the original data:", missing_indices.tolist())

    # Reindex the DataFrame based on the target_patients' stay_id
    df = df.reindex(target_patients['stay_id']).reset_index()

def reindex(file_path, sorted_path):
    sorted_data = sort_patient_data(file_path)  
    sorted_data.to_csv(sorted_path, index=False) 

if __name__ == "__main__":
    reindex(file_path, sorted_path)  