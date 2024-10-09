from pathlib import Path

DEMO_RUNS_DIR = Path(__file__).resolve().parent
DEMO_QUERIES_DIR = DEMO_RUNS_DIR.parent / 'demographics_queries'
DEMO_RESULTS_DIR = DEMO_RUNS_DIR.parent / 'demographics_results'

# Ensure the demographics_results folder exists
DEMO_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print(f"Demographics Runs Directory: {DEMO_RUNS_DIR}")
print(f"Demographics Queries Directory: {DEMO_QUERIES_DIR}")
print(f"Demographics Results Directory: {DEMO_RESULTS_DIR}")
