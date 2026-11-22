# Uniform Cost Search (UCS) 

## 1. Algorithm Description

Uniform Cost Search (UCS) is an uninformed search algorithm that finds the path with the lowest total travel cost from a starting location to a goal location.

In OptiMap, each edge represents a two-way road, and its cost represents travel time in minutes.

UCS uses a Priority Queue implemented with Python's `heapq` library. The node with the lowest cumulative path cost is always selected first.

The algorithm uses three main data structures:

- **Priority Queue:** Stores nodes according to their cumulative travel cost.
- **Cost Dictionary (`cost_so_far`):** Stores the cheapest known cost to reach each location.
- **Parent Dictionary (`parent`):** Stores the previous location for each node to reconstruct the final path.

When a cheaper route to an already discovered location is found, UCS updates its cost and parent and inserts a new entry into the Priority Queue.

Outdated entries are ignored when removed from the queue.

When the goal is reached, the algorithm reconstructs the path using the Parent Dictionary and calculates the total travel cost.

## 2. Pseudocode

```text
UCS(graph, start, goal):

    Create an empty Priority Queue
    Insert start with cost 0

    cost_so_far[start] = 0
    parent[start] = None

    Initialize generated, expanded, and frontier measurements

    WHILE Priority Queue is not empty:

        Remove the node with the lowest cost

        IF the entry is outdated:
            CONTINUE

        IF current node is the goal:
            Reconstruct the path using parent
            Calculate total path cost
            Return the result

        Increase nodes_expanded

        FOR each neighbor of the current node:

            new_cost = current_cost + road_cost

            IF new_cost is cheaper than the known cost:

                Update cost_so_far[neighbor]
                Update parent[neighbor]

                Insert neighbor into Priority Queue
                Increase nodes_generated

        Update maximum frontier size

    Return failure result
```

## 3. Data Structures

| Data Structure | Purpose |
|---|---|
| Priority Queue (`heapq`) | Selects the lowest-cost node |
| Cost Dictionary | Stores the cheapest known cost |
| Parent Dictionary | Reconstructs the solution path |
| Counter | Handles equal-cost priority queue entries |

## 4. Complexity Analysis

### General UCS Properties

| Property | Description |
|---|---|
| Search Type | Uninformed Search |
| Complete | Yes, when step costs have a positive minimum |
| Optimal | Yes, with nonnegative edge costs |
| Node Selection | Lowest cumulative path cost |
| Data Structure | Priority Queue |

### Complexity for the OptiMap Implementation

Let:
- V = Number of locations (vertices).
- E = Number of roads (edges).

Using an adjacency-list graph and a heap-based Priority Queue with lazy duplicate entries:

| Property | Complexity |
|---|---|
| Time Complexity | O((V + E) log E) |
| Space Complexity | O(V + E) |

The space complexity includes the graph, dictionaries, and Priority Queue entries.

## 5. Performance Measurements

The UCS implementation records four main measurements:

1. **Nodes Generated:** Number of nodes inserted into the Priority Queue, including the starting node.
2. **Nodes Expanded:** Number of valid nodes removed from the Priority Queue whose neighbors are examined.
3. **Maximum Frontier Size:** Maximum number of pending Priority Queue entries.
4. **Running Time:** Total execution time measured using Python's `time.perf_counter()`.

The frontier size includes outdated entries until they are removed from the Priority Queue.

## 6. Result Format

The algorithm returns the shared result structure defined in `src/core/result_schema.py`.

The returned fields are:

- `algorithm`
- `found`
- `path`
- `path_cost`
- `nodes_generated`
- `nodes_expanded`
- `max_frontier_size`
- `running_time`

If the goal cannot be reached, the algorithm returns `found = False`, an empty path, and an infinite path cost.

## 7. Dataset Configuration

The primary OptiMap experiment uses:

| Setting | Value |
|---|---|
| Dataset | 5,000 locations |
| Roads | 9,850 undirected roads |
| Starting Location | N0001 |
| Goal Location | N5000 |
| Edge Cost | Travel time in minutes |

The same starting and goal locations are used for comparison with the other search algorithms.

## 8. Conclusion

Uniform Cost Search finds the lowest-cost route by expanding locations in increasing order of cumulative travel time.

The Priority Queue ensures that the cheapest available route is considered first. The Cost Dictionary allows the algorithm to update previously discovered locations when a cheaper route is found, while the Parent Dictionary reconstructs the final solution.

UCS is suitable for OptiMap because the objective is to find routes with minimum total travel time rather than simply minimizing the number of roads.
