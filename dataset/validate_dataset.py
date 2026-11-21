import csv
from pathlib import Path
from collections import defaultdict, deque

# Get the directory containing this Python file
DATASET_DIR = Path(__file__).resolve().parent

# Read dataset
with open(DATASET_DIR / "locations.csv",
          newline="", encoding="utf-8") as f:
    locations = list(csv.DictReader(f))

with open(DATASET_DIR / "roads.csv",
          newline="", encoding="utf-8") as f:
    roads = list(csv.DictReader(f))


location_ids = [loc["location_id"] for loc in locations]
location_set = set(location_ids)

# Test 1: Number of locations
assert len(locations) == 5000, "Wrong number of locations!"

# Test 2: Unique IDs
assert len(location_set) == 5000, "Duplicate location IDs!"

# Build an undirected graph
graph = defaultdict(list)

for road in roads:
    u = road["from_location"]
    v = road["to_location"]
    cost = float(road["travel_time_min"])

    # Test 3: Road endpoints exist
    assert u in location_set and v in location_set, \
        f"Unknown location in road {road['road_id']}"

    # Test 4: Positive cost
    assert cost > 0, f"Invalid cost in road {road['road_id']}"

    graph[u].append(v)
    graph[v].append(u)

# Test 5: Number of roads
assert len(roads) == 9850, "Wrong number of roads!"

# Test 6: Connectivity using BFS
start = location_ids[0]
visited = {start}
queue = deque([start])

while queue:
    current = queue.popleft()

    for neighbor in graph[current]:
        if neighbor not in visited:
            visited.add(neighbor)
            queue.append(neighbor)

assert len(visited) == 5000, \
    f"Graph is disconnected! Reached only {len(visited)} nodes."

print("ALL DATASET TESTS PASSED!")
print("Locations:", len(locations))
print("Roads:", len(roads))
print("Reachable locations:", len(visited))
