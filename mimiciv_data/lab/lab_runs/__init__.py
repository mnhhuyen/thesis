from pathlib import Path

LAB_RUNS_DIR = Path(__file__).resolve().parent
LAB_QUERIES_DIR = LAB_RUNS_DIR.parent / 'lab_queries'
LAB_RESULTS_DIR = LAB_RUNS_DIR.parent / 'lab_results'

# Ensure the demographics_results folder exists
LAB_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print(f"Lab Runs Directory: {LAB_RUNS_DIR}")
print(f"Lab Queries Directory: {LAB_QUERIES_DIR}")
print(f"Lab Results Directory: {LAB_RESULTS_DIR}")
