
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


COLORS = {
    "roads": "#C9CED6",
    "unexplored": "#AAB2BD",
    "explored": "#2878B5",
    "frontier": "#F2C14E",
    "path": "#8A45B5",
    "start": "#2E9D57",
    "goal": "#D64545",
}


def _build_coordinates(locations):
    coords = {}

    for location in locations:
        node = location["location_id"]

        if node in coords:
            raise ValueError(f"Duplicate location ID: {node}")

        try:
            coords[node] = (
                float(location["x_km"]),
                float(location["y_km"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(
                f"Location {node!r} must have numeric x_km and y_km"
            ) from exc

    if not coords:
        raise ValueError("The locations dataset is empty")

    return coords


def _get_edges(roads=None, graph=None):
    if roads is None and graph is None:
        raise ValueError("Pass either roads or graph")

    if roads is not None:
        source = (
            (road["from_location"], road["to_location"])
            for road in roads
        )
    else:
        source = (
            (node, neighbor)
            for node, neighbors in graph.items()
            for neighbor in neighbors
        )

    edges = []
    seen = set()

    for u, v in source:
        if u == v:
            continue

        key = tuple(sorted((u, v)))

        if key not in seen:
            seen.add(key)
            edges.append((u, v))

    return edges


def _validate_nodes(nodes, coords, field_name):
    unknown = set(nodes) - set(coords)

    if unknown:
        sample = sorted(unknown)[:5]
        raise ValueError(
            f"{field_name} contains unknown location IDs: {sample}"
        )


def plot_map(
    locations,
    roads=None,
    result=None,
    start=None,
    goal=None,
    save_path=None,
    show=True,
    graph=None,
    explored_nodes=None,
    frontier_nodes=None,
    title="OptiMap - City Road Network",
    figsize=(13, 9),
):

    result = result or {}
    coords = _build_coordinates(locations)
    edges = _get_edges(roads=roads, graph=graph)

    for u, v in edges:
        _validate_nodes((u, v), coords, "Road endpoints")

    path = (
        list(result.get("path") or [])
        if result.get("found")
        else []
    )

    if start is None:
        start = result.get("start") or (
            path[0] if path else None
        )

    if goal is None:
        goal = result.get("goal") or (
            path[-1] if path else None
        )

    explored = set(
        explored_nodes
        if explored_nodes is not None
        else result.get(
            "explored_nodes",
            result.get("exploration_order", [])
        )
    )

    frontier = set(
        frontier_nodes
        if frontier_nodes is not None
        else result.get("frontier_nodes", [])
    )

    _validate_nodes(explored, coords, "Explored nodes")
    _validate_nodes(frontier, coords, "Frontier nodes")
    _validate_nodes(path, coords, "Path")

    if start is not None:
        _validate_nodes([start], coords, "Start")

    if goal is not None:
        _validate_nodes([goal], coords, "Goal")

    edge_set = {
        tuple(sorted(edge))
        for edge in edges
    }

    for u, v in zip(path, path[1:]):
        if tuple(sorted((u, v))) not in edge_set:
            raise ValueError(
                f"Path contains a non-existent road: {u} - {v}"
            )

    fig, ax = plt.subplots(figsize=figsize)

    road_segments = [
        [coords[u], coords[v]]
        for u, v in edges
    ]

    if road_segments:
        ax.add_collection(
            LineCollection(
                road_segments,
                colors=COLORS["roads"],
                linewidths=0.55,
                alpha=0.75,
                zorder=1,
            )
        )

    all_x = [
        point[0]
        for point in coords.values()
    ]

    all_y = [
        point[1]
        for point in coords.values()
    ]

    ax.scatter(
        all_x,
        all_y,
        s=7,
        c=COLORS["unexplored"],
        alpha=0.75,
        label="Locations",
        zorder=2,
    )

    def draw_nodes(nodes, color, label, size, zorder):
        nodes = sorted(set(nodes))

        if nodes:
            ax.scatter(
                [coords[node][0] for node in nodes],
                [coords[node][1] for node in nodes],
                s=size,
                c=color,
                label=label,
                edgecolors="white",
                linewidths=0.25,
                zorder=zorder,
            )

    draw_nodes(
        explored,
        COLORS["explored"],
        "Explored",
        15,
        3,
    )

    draw_nodes(
        frontier - explored - set(path),
        COLORS["frontier"],
        "Frontier",
        22,
        4,
    )

    if len(path) >= 2:
        path_segments = [
            [coords[u], coords[v]]
            for u, v in zip(path, path[1:])
        ]

        ax.add_collection(
            LineCollection(
                path_segments,
                colors=COLORS["path"],
                linewidths=3.0,
                label="Final path",
                zorder=5,
            )
        )

        draw_nodes(
            path,
            COLORS["path"],
            "Path locations",
            25,
            6,
        )

    draw_nodes(
        [start] if start else [],
        COLORS["start"],
        "Start",
        95,
        8,
    )

    draw_nodes(
        [goal] if goal else [],
        COLORS["goal"],
        "Goal",
        95,
        9,
    )

    algorithm = result.get("algorithm")

    display_title = (
        title
        if not algorithm
        else f"{title} | {algorithm}"
    )

    ax.set_title(display_title)
    ax.set_xlabel("X coordinate (km)")
    ax.set_ylabel("Y coordinate (km)")
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(alpha=0.18)
    ax.legend(loc="best", fontsize=8)

    fig.tight_layout()

    if save_path is not None:
        output = Path(save_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        fig.savefig(
            output,
            dpi=200,
            bbox_inches="tight",
        )

    if show:
        plt.show()

    return fig, ax
