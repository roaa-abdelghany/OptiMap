
"""Main entry point for OptiMap."""

from src.problem.graph_builder import load_graph
from src.core.config import DATASET_DIR, START, GOAL
from src.problem.problem_model import OptiMapProblem


def main():
    # Load the real city dataset and build the graph
    locations, roads, graph = load_graph(DATASET_DIR)

    # Create the search problem
    problem = OptiMapProblem(
        graph=graph,
        start=START,
        goal=GOAL
    )

    print("OptiMap loaded successfully.")
    print(f"Number of locations: {len(graph)}")
    print(f"Start: {problem.start}")
    print(f"Goal: {problem.goal}")


if __name__ == "__main__":
    main()
