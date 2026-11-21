import json
from pathlib import Path

def load_dataset(dataset_dir):
    dataset_dir = Path(dataset_dir)
    with (dataset_dir / "locations.json").open(encoding="utf-8") as f:
        locations = json.load(f)
    with (dataset_dir / "roads.json").open(encoding="utf-8") as f:
        roads = json.load(f)
    return locations, roads

def build_graph(locations, roads):
    """Return graph[node][neighbor] = travel_time_min; roads are two-way."""
    graph = {loc["location_id"]: {} for loc in locations}
    for road in roads:
        u, v = road["from_location"], road["to_location"]
        cost = float(road["travel_time_min"])
        if u not in graph or v not in graph:
            raise ValueError(f"Road {road.get('road_id')} references an unknown location")
        if cost <= 0:
            raise ValueError(f"Road {road.get('road_id')} has non-positive cost")
        if v in graph[u] or u in graph[v]:
            raise ValueError(f"Duplicate road between {u} and {v}")
        graph[u][v] = cost
        graph[v][u] = cost
    return graph

def load_graph(dataset_dir):
    locations, roads = load_dataset(dataset_dir)
    return locations, roads, build_graph(locations, roads)
