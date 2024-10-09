from pathlib import Path

COM_RUNS_DIR = Path(__file__).resolve().parent
COM_QUERIES_DIR = COM_RUNS_DIR.parent / 'comorbidity_queries'
COM_RESULTS_DIR = COM_RUNS_DIR.parent / 'comorbidity_results'

# Ensure the demographics_results folder exists
COM_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print(f"Comorbidity Runs Directory: {COM_RUNS_DIR}")
print(f"Comorbidity Queries Directory: {COM_QUERIES_DIR}")
print(f"Comorbidity Results Directory: {COM_RESULTS_DIR}")
