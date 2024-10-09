from run_queries.age import run_derived_data as run_age_data
from run_queries.bg import run_derived_data as run_bg_data
from run_queries.blood_count import run_derived_data as run_bc_data
from run_queries.blood_differential import run_derived_data as run_bd_data
from run_queries.cardiac_marker import run_derived_data as run_cm_data
from run_queries.chemistry import run_derived_data as run_chem_data
from run_queries.coagulation import run_derived_data as run_coag_data
from run_queries.dobutamine import run_derived_data as run_db_data
from run_queries.dopamine import run_derived_data as run_dp_data
from run_queries.enzyme import run_derived_data as run_enz_data
from run_queries.epinephrine import run_derived_data as run_ep_data
from run_queries.first_day_gcs import run_derived_data as run_fdg_data
from run_queries.first_day_lab import run_derived_data as run_fdl_data
from run_queries.first_day_urine_output import run_derived_data as run_fdu_data
from run_queries.first_day_vitalsign import run_derived_data as run_fdv_data
from run_queries.gcs import run_derived_data as run_gcs_data
from run_queries.height import run_derived_data as run_height_data
from run_queries.icustay_hourly import run_derived_data as run_ihourly_data
from run_queries.icustay_times import run_derived_data as run_itimes_data
from run_queries.lods import run_derived_data as run_lods_data
from run_queries.norepinephrine import run_derived_data as run_norep_data
from run_queries.oxygen_delivery import run_derived_data as run_oxy_data
from run_queries.sapsii import run_derived_data as run_sapsii_data
from run_queries.sofa import run_derived_data as run_sofa_data
from run_queries.urine_output_rate import run_derived_data as run_uor_data
from run_queries.urine_output import run_derived_data as run_uo_data
from run_queries.ventilation_classification import run_derived_data as run_ventc_data
from run_queries.ventilation_durations import run_derived_data as run_ventd_data
from run_queries.ventilator_settings import run_derived_data as run_vents_data
from run_queries.ventilation import run_derived_data as run_vent_data
from run_queries.vitalsigns import run_derived_data as run_vs_data
from run_queries.weight_durations import run_derived_data as run_weight_data

def get_derived_data():
    tasks = [
        ("age derived data", run_age_data),
        ("height data", run_height_data),
        ("weight durations data", run_weight_data),
        ("GCS data", run_gcs_data),
        ("oxygen delivery data", run_oxy_data),
        ("ventilation classification data", run_ventc_data),
        ("ventilation durations data", run_ventd_data),
        ("ventilator settings data", run_vents_data),
        ("ventilation data", run_vent_data),
        ("vitalsigns data", run_vs_data),
        ("urine output data", run_uo_data),
        ("urine output rate data", run_uor_data),
        ("bg derived data", run_bg_data),
        ("blood count data", run_bc_data),
        ("blood differential data", run_bd_data),
        ("cardiac marker data", run_cm_data),
        ("chemistry data", run_chem_data),
        ("coagulation data", run_coag_data),
        ("dobutamine data", run_db_data),
        ("dopamine data", run_dp_data),
        ("enzyme data", run_enz_data),
        ("epinephrine data", run_ep_data),
        ("norepinephrine data", run_norep_data),
        ("first day GCS data", run_fdg_data),
        ("first day lab data", run_fdl_data),
        ("first day urine output data", run_fdu_data),
        ("first day vitalsign data", run_fdv_data),
        ("ICU stay times data", run_itimes_data),
        ("ICU stay hourly data", run_ihourly_data),
        ("LODS data", run_lods_data),
        ("SAPS-II data", run_sapsii_data),
        ("SOFA data", run_sofa_data),
    ]
    
    for task_name, task_func in tasks:
        print(f"Running {task_name}")
        task_func()
        print(f"Finished {task_name}")

if __name__ == "__main__":
    get_derived_data()
