
import time

from src.core.result_schema import make_result


def depth_limited_search(graph, start, goal, depth_limit):
    frontier = [(start, 0, (start,))]
    parent_nodes = {(start,): None}

    nodes_generated = 1
    nodes_expanded = 0
    max_frontier_size = 1

    while frontier:
        current, depth, path = frontier.pop()

        if current == goal:
            solution_path = []
            path_node = path

            while path_node is not None:
                solution_path.append(path_node[-1])
                path_node = parent_nodes[path_node]

            solution_path.reverse()

            return {
                "found": True,
                "path": solution_path,
                "nodes_generated": nodes_generated,
                "nodes_expanded": nodes_expanded,
                "max_frontier_size": max_frontier_size,
                "cutoff": False
            }

        if depth == depth_limit:
            continue

        nodes_expanded += 1

        neighbors = list(graph.get(current, {}).items())

        for neighbor, cost in reversed(neighbors):
            if neighbor in path:
                continue

            new_path = path + (neighbor,)
            parent_nodes[new_path] = path

            frontier.append(
                (neighbor, depth + 1, new_path)
            )

            nodes_generated += 1

        max_frontier_size = max(
            max_frontier_size,
            len(frontier)
        )

    return {
        "found": False,
        "path": [],
        "nodes_generated": nodes_generated,
        "nodes_expanded": nodes_expanded,
        "max_frontier_size": max_frontier_size,
        "cutoff": False
    }


def search(graph, start, goal):
    start_time = time.perf_counter()

    total_generated = 0
    total_expanded = 0
    max_frontier_size = 0

    max_depth = max(0, len(graph) - 1)

    for depth_limit in range(max_depth + 1):
        result = depth_limited_search(
            graph,
            start,
            goal,
            depth_limit
        )

        total_generated += result["nodes_generated"]
        total_expanded += result["nodes_expanded"]

        max_frontier_size = max(
            max_frontier_size,
            result["max_frontier_size"]
        )

        if result["found"]:
            path = result["path"]

            path_cost = sum(
                graph[path[i]][path[i + 1]]
                for i in range(len(path) - 1)
            )

            running_time = time.perf_counter() - start_time

            return make_result(
                algorithm="IDS",
                found=True,
                path=path,
                path_cost=path_cost,
                nodes_generated=total_generated,
                nodes_expanded=total_expanded,
                max_frontier_size=max_frontier_size,
                running_time=running_time
            )

    running_time = time.perf_counter() - start_time

    return make_result(
        algorithm="IDS",
        found=False,
        path=[],
        path_cost=float("inf"),
        nodes_generated=total_generated,
        nodes_expanded=total_expanded,
        max_frontier_size=max_frontier_size,
        running_time=running_time
    )
