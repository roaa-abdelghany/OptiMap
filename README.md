# OptiMap – Phase I shared foundation

## Dataset
- 5,000 locations (`dataset/locations.json`)
- 9,850 undirected two-way roads (`dataset/roads.json`)
- 19,700 directed adjacency entries after graph construction
- Travel-time edge costs are in minutes.
- CSV copies are included for spreadsheet inspection.

## Setup
Python 3.9+ is recommended. No third-party package is needed for the foundation smoke test.
```bash
python main.py
```

## Shared contracts
- `build_graph` returns `graph[node][neighbor] = travel_time_min`.
- All roads are two-way and are inserted in both directions.
- Each algorithm must implement `search(graph, start, goal)` and return the keys in `src/core/result_schema.py`.
- Use the common START and GOAL in `src/core/config.py` for the primary comparison.
- Metrics definitions: generated = states inserted/produced by the algorithm according to its documented duplicate policy; expanded = states removed from frontier and whose successors are examined; max frontier = maximum number of pending frontier entries. Document any algorithm-specific counting convention clearly.

## Team implementation
Implement BFS, DFS, UCS and IDS yourselves in `src/algorithms/`. Ready-made search algorithms are not allowed by the project brief. Visualization and data-handling libraries are allowed.

## Validation
Run `python validate_foundation.py` to verify node/road counts, endpoint validity, positive costs, two-way adjacency, and connectivity on the included real dataset.
