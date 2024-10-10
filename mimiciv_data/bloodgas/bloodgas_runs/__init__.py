from pathlib import Path

BG_RUNS_DIR = Path(__file__).resolve().parent
BG_QUERIES_DIR = BG_RUNS_DIR.parent / 'bloodgas_queries'
BG_RESULTS_DIR = BG_RUNS_DIR.parent / 'bloodgas_results'

# Ensure the demographics_results folder exists
BG_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print(f"BG Runs Directory: {BG_RUNS_DIR}")
print(f"BG Queries Directory: {BG_QUERIES_DIR}")
print(f"BG Results Directory: {BG_RESULTS_DIR}")
