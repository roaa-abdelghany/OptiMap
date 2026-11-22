
import heapq
import time
from itertools import count


def search(graph, start, goal):
    start_time = time.perf_counter()
    frontier = []
    counter = count()
    heapq.heappush(frontier, (0, next(counter), start))
    cost_so_far = {start: 0}
    parent = {start: None}

    nodes_generated = 1
    nodes_expanded = 0
    max_frontier_size = 1

    while frontier:

        current_cost, _, current = heapq.heappop(frontier)
        if current_cost != cost_so_far.get(current):
            continue
        if current == goal:
            path = []
            node = goal
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            running_time = time.perf_counter() - start_time
            return {
                "algorithm": "UCS",
                "found": True,
                "path": path,
                "path_cost": current_cost,
                "nodes_generated": nodes_generated,
                "nodes_expanded": nodes_expanded,
                "max_frontier_size": max_frontier_size,
                "running_time": running_time
            }

        nodes_expanded += 1
        for neighbor, road_cost in graph.get(current, {}).items():
            new_cost = current_cost + road_cost
            if new_cost < cost_so_far.get(neighbor, float("inf")):
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(
                    frontier,
                    (new_cost, next(counter), neighbor)
                )
                nodes_generated += 1
              
        max_frontier_size = max(max_frontier_size, len(frontier))

    running_time = time.perf_counter() - start_time
    return {
        "algorithm": "UCS",
        "found": False,
        "path": [],
        "path_cost": float("inf"),
        "nodes_generated": nodes_generated,
        "nodes_expanded": nodes_expanded,
        "max_frontier_size": max_frontier_size,
        "running_time": running_time
    }
