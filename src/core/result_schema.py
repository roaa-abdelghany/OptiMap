REQUIRED_RESULT_KEYS = (
    "algorithm", "found", "path", "path_cost", "nodes_generated",
    "nodes_expanded", "max_frontier_size", "running_time"
)

def make_result(algorithm, found=False, path=None, path_cost=float("inf"),
                nodes_generated=0, nodes_expanded=0, max_frontier_size=0,
                running_time=0.0):
    return {
        "algorithm": algorithm, "found": bool(found), "path": path or [],
        "path_cost": float(path_cost), "nodes_generated": int(nodes_generated),
        "nodes_expanded": int(nodes_expanded),
        "max_frontier_size": int(max_frontier_size),
        "running_time": float(running_time)
    }

def validate_result(result):
    missing = set(REQUIRED_RESULT_KEYS) - set(result)
    if missing:
        raise ValueError(f"Missing result fields: {sorted(missing)}")
    return result
