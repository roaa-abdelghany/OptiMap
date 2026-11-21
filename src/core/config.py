from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = ROOT / "dataset"
RESULTS_DIR = ROOT / "results"
START = "N0001"
GOAL = "N5000"
EXPECTED_LOCATIONS = 5000
EXPECTED_ROADS = 9850
