import pandas as pd

from config.config_param import mimic_path, target_patients_path 

target_patients = pd.read_csv(target_patients_path)
def sort_patient_data(file_path):
    df = pd.read_csv(file_path)
    df = df.set_index('stay_id').reindex(target_patients).reset_index()

    return df

def reindex(file_path, sorted_file_path):
    sorted_data = sort_patient_data(file_path)
    sorted_data.to_csv(sorted_file_path)
