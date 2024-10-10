import pandas as pd
import os
from config.config_param import target_patients_path, mimiciv_data_path, sorted_data_path

sorted_path = sorted_data_path

list_file_path = [
    os.path.join(mimiciv_data_path, 'demographics/demographics_results/race_output.csv'),
    os.path.join(mimiciv_data_path, 'demographics/demographics_results/gender_output.csv'),
    os.path.join(mimiciv_data_path, 'demographics/demographics_results/height_output.csv'),
    os.path.join(mimiciv_data_path, 'demographics/demographics_results/weight_output.csv'),
    os.path.join(mimiciv_data_path, 'demographics/demographics_results/bmi_output.csv'),
    os.path.join(mimiciv_data_path, 'demographics/demographics_results/gcs_output.csv'),
    os.path.join(mimiciv_data_path, 'demographics/demographics_results/duration_mv_output.csv'),
    os.path.join(mimiciv_data_path, 'vitalsigns/vitalsigns_results/vitalsign_output.csv'),
    os.path.join(mimiciv_data_path, 'vitalsigns/vitalsigns_results/urine_output_output.csv'),
    os.path.join(mimiciv_data_path, 'vitalsigns/vitalsigns_results/vitalsign_output.csv'),
    os.path.join(mimiciv_data_path, 'bloodgas/bloodgas_results/bg_output.csv'),
    os.path.join(mimiciv_data_path, 'lab/lab_results/lab_output.csv'),
    os.path.join(mimiciv_data_path, 'comorbidity/comorbidity_results/patients_with_comorbidity.csv'),
    os.path.join(mimiciv_data_path, 'scores/score_results/score_output.csv')
]

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
    return df.reindex(target_patients['stay_id']).reset_index()

def reindex(file_path, sorted_path):
    sorted_data = sort_patient_data(file_path)
    
    file_name = os.path.basename(file_path)
    sorted_data.to_csv(os.path.join(sorted_path, file_name), index=False) 

if __name__ == "__main__":
    for file_path in list_file_path:
        reindex(file_path, sorted_path)  