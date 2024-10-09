import pandas as pd
import os
from config.config_param import target_patients_path

file_path = '/media/data/huyennm/mimic-iv/notebook/demographics/demographics_results/race_output.csv'
sorted_path = '/media/data/huyennm/mimic-iv/notebook/demographics/demographics_runs/sorted.csv'

target_patients = pd.read_csv(target_patients_path)

def sort_patient_data(file_path):
    df = pd.read_csv(file_path) 
    df = df.set_index('stay_id').reindex(target_patients['stay_id']).reset_index()  
    return df

def reindex(file_path, sorted_path):
    sorted_data = sort_patient_data(file_path)  
    sorted_data.to_csv(sorted_path, index=False) 

if __name__ == "__main__":
    reindex(file_path, sorted_path)  