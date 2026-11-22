import time

from src.core.result_schema import make_result


def _reconstruct_path(parent, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path


def _path_cost(graph, path):
    return sum(float(graph[u][v]) for u, v in zip(path, path[1:]))


def search(graph, start, goal):
    if start not in graph:
        raise ValueError(f"Unknown start location: {start}")
    if goal not in graph:
        raise ValueError(f"Unknown goal location: {goal}")

    started = time.perf_counter()
    frontier = [start]
    discovered = {start}
    parent = {start: None}
    nodes_generated = 1
    nodes_expanded = 0
    max_frontier_size = 1
    exploration_order = []

    while frontier:
        current = frontier.pop()
        exploration_order.append(current)

        if current == goal:
            path = _reconstruct_path(parent, goal)
            elapsed = time.perf_counter() - started
            result = make_result(
                algorithm="DFS", found=True, path=path,
                path_cost=_path_cost(graph, path),
                nodes_generated=nodes_generated,
                nodes_expanded=nodes_expanded,
                max_frontier_size=max_frontier_size,
                running_time=elapsed,
            )
            result["exploration_order"] = exploration_order
            return result

        nodes_expanded += 1
        for neighbor in sorted(graph.get(current, {}), reverse=True):
            if neighbor not in discovered:
                discovered.add(neighbor)
                parent[neighbor] = current
                frontier.append(neighbor)
                nodes_generated += 1
        max_frontier_size = max(max_frontier_size, len(frontier))

    elapsed = time.perf_counter() - started
    result = make_result(
        algorithm="DFS", found=False, path=[], path_cost=float("inf"),
        nodes_generated=nodes_generated, nodes_expanded=nodes_expanded,
        max_frontier_size=max_frontier_size, running_time=elapsed,
    )
    result["exploration_order"] = exploration_order
    return result
