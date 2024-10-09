import os
import sys
import pandas as pd
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from demographics_runs import DEMO_RESULTS_DIR
from config.config_param import mimic_path, target_patients_path 

def add_bmi(target_patients):
    target_patients['bmi'] = target_patients.apply(
        lambda row: round(row['weight_admit'] / ((row['height'] / 100) ** 2), 2)
        if pd.notnull(row['weight_admit']) and pd.notnull(row['height']) and row['height'] > 0 else
        (round(row['weight'] / ((row['height'] / 100) ** 2), 2)
        if pd.notnull(row['weight']) and pd.notnull(row['height']) and row['height'] > 0 else None),
        axis=1
    )
    return target_patients

def add_bmi_omr(target, bmi_omr):
    for index, row in target[target['bmi'].isna()].iterrows():
        records = bmi_omr[bmi_omr['subject_id'] == row['subject_id']]
        # print(f"Found {len(records)} matching records in bmi_omr for subject_id {row['subject_id']}")
        
        if not records.empty:
            records['time_diff'] = abs(pd.to_datetime(records['chartdate']) - pd.to_datetime(row['starttime']))
            closest_bmi_record = records.loc[records['time_diff'].idxmin()]
            target.at[index, 'bmi'] = closest_bmi_record['result_value']
    return target

def merge_height_weight(target_patients, height_output_path, weight_output_path):
    """
    Load and merge height and weight data into target_patients.
    
    Args:
        target_patients (DataFrame): The target patients DataFrame.
        height_output_path (str): Path to the height_output.csv file.
        weight_output_path (str): Path to the weight_output.csv file.
        
    Returns:
        DataFrame: The target_patients DataFrame with height, weight_admit, and weight columns.
    """
    height_df = pd.read_csv(height_output_path)
    weight_df = pd.read_csv(weight_output_path)

    target_patients = pd.merge(target_patients, height_df[['subject_id', 'stay_id', 'height']], on=['subject_id', 'stay_id'], how='left')

    target_patients = pd.merge(target_patients, weight_df[['subject_id', 'stay_id', 'weight_admit', 'weight']], on=['subject_id', 'stay_id'], how='left')

    return target_patients

def run_bmi_processing():
    target_patients = pd.read_csv(target_patients_path)

    omr_path = os.path.join(mimic_path, 'hosp/omr.csv')
    omr = pd.read_csv(omr_path)
    
    bmi_omr = omr[(omr['result_name'] == 'BMI (kg/m2)') & (omr['subject_id'].isin(target_patients['subject_id']))]
    
    height_output_path = DEMO_RESULTS_DIR / 'height_output.csv'
    weight_output_path = DEMO_RESULTS_DIR / 'weight_output.csv'
    target_patients = merge_height_weight(target_patients, height_output_path, weight_output_path)

    target_patients = add_bmi(target_patients)

    target_patients = add_bmi_omr(target_patients, bmi_omr)
    
    output_csv = DEMO_RESULTS_DIR / 'bmi_output.csv'
    target_patients.to_csv(output_csv, index=False)
    print(f"Result saved to {output_csv}")

if __name__ == "__main__":
    run_bmi_processing()
