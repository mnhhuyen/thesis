from pathlib import Path

VITAL_RUNS_DIR = Path(__file__).resolve().parent
VITAL_QUERIES_DIR = VITAL_RUNS_DIR.parent / 'vitalsigns_queries'
VITAL_RESULTS_DIR = VITAL_RUNS_DIR.parent / 'vitalsigns_results'

# Ensure the demographics_results folder exists
VITAL_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print(f"Vital Runs Directory: {VITAL_RUNS_DIR}")
print(f"Vital Queries Directory: {VITAL_QUERIES_DIR}")
print(f"Vital Results Directory: {VITAL_RESULTS_DIR}")
