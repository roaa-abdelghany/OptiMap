from src.problem.graph_builder import load_graph
from src.problem.graph_validator import validate_dataset
from src.core.config import DATASET_DIR, EXPECTED_LOCATIONS, EXPECTED_ROADS

if __name__ == "__main__":
    locations, roads, graph = load_graph(DATASET_DIR)
    report = validate_dataset(locations, roads, graph, EXPECTED_LOCATIONS, EXPECTED_ROADS)
    print("PASS: OptiMap dataset and graph validation")
    for key, value in report.items():
        print(f"{key}: {value}")
