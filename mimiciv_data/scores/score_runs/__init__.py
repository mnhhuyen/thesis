from pathlib import Path

SCORE_RUNS_DIR = Path(__file__).resolve().parent
SCORE_QUERIES_DIR = SCORE_RUNS_DIR.parent / 'score_queries'
SCORE_RESULTS_DIR = SCORE_RUNS_DIR.parent / 'score_results'

SCORE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print(f"Score Runs Directory: {SCORE_RUNS_DIR}")
print(f"Score Queries Directory: {SCORE_QUERIES_DIR}")
print(f"Score Results Directory: {SCORE_RESULTS_DIR}")
