"""Validation utilities for the real OptiMap dataset."""
from collections import deque

def validate_dataset(locations, roads, graph, expected_nodes=5000, expected_roads=9850):
    ids = [x["location_id"] for x in locations]
    assert len(ids) == expected_nodes, f"Expected {expected_nodes} locations, got {len(ids)}"
    assert len(set(ids)) == len(ids), "Duplicate location IDs"
    id_set = set(ids)
    assert len(roads) == expected_roads, f"Expected {expected_roads} roads, got {len(roads)}"
    assert set(graph) == id_set, "Graph node set differs from locations"
    for r in roads:
        u, v = r["from_location"], r["to_location"]
        assert u in id_set and v in id_set, f"Unknown endpoint in {r['road_id']}"
        c = float(r["travel_time_min"])
        assert c > 0, f"Non-positive cost in {r['road_id']}"
        assert graph[u].get(v) == c and graph[v].get(u) == c, f"Missing/wrong two-way edge: {r['road_id']}"
    start = ids[0]
    seen, q = {start}, deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in seen:
                seen.add(v); q.append(v)
    assert len(seen) == expected_nodes, f"Graph disconnected: reached {len(seen)} / {expected_nodes}"
    arc_count = sum(len(nbrs) for nbrs in graph.values())
    assert arc_count == 2 * expected_roads, f"Expected {2*expected_roads} directed arcs, got {arc_count}"
    return {"locations": len(ids), "roads": len(roads), "directed_arcs": arc_count,
            "reachable_locations": len(seen), "min_cost": min(float(r["travel_time_min"]) for r in roads),
            "max_cost": max(float(r["travel_time_min"]) for r in roads)}
