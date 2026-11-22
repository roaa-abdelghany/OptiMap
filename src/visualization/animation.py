
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection

from src.visualization.visualizer import (
    COLORS,
    _build_coordinates,
    _get_edges,
    _validate_nodes,
)


def _normalise_trace(search_trace):

    if not search_trace:
        raise ValueError(
            "search_trace is empty; no search steps to animate"
        )

    events = []

    for item in search_trace:

        if isinstance(item, str):
            events.append({
                "node": item,
                "frontier": [],
            })

        elif isinstance(item, dict) and "node" in item:
            events.append({
                "node": item["node"],
                "frontier": list(item.get("frontier", [])),
            })

        else:
            raise ValueError(
                "Each trace item must be a location ID or a dictionary "
                "containing 'node' and optional 'frontier'"
            )

    return events


def animate_search(
    locations,
    roads=None,
    search_trace=None,
    result=None,
    start=None,
    goal=None,
    interval=120,
    save_path=None,
    show=True,
    graph=None,
    max_frames=500,
    repeat=False,
    figsize=(13, 9),
):

    result = result or {}

    if search_trace is None:
        search_trace = result.get("search_trace")

    if search_trace is None:
        search_trace = result.get("exploration_order")

    if search_trace is None:
        raise ValueError(
            "No search trace found. The algorithm must return "
            "'search_trace' or 'exploration_order'."
        )

    events = _normalise_trace(search_trace)

    coords = _build_coordinates(locations)
    edges = _get_edges(roads=roads, graph=graph)

    for u, v in edges:
        _validate_nodes(
            (u, v),
            coords,
            "Road endpoints"
        )

    for event in events:
        _validate_nodes(
            [event["node"]],
            coords,
            "Trace node"
        )

        _validate_nodes(
            event["frontier"],
            coords,
            "Trace frontier"
        )

    path = (
        list(result.get("path") or [])
        if result.get("found")
        else []
    )

    _validate_nodes(path, coords, "Final path")

    start = (
        start
        or result.get("start")
        or (path[0] if path else events[0]["node"])
    )

    goal = (
        goal
        or result.get("goal")
        or (path[-1] if path else None)
    )

    if start is not None:
        _validate_nodes([start], coords, "Start")

    if goal is not None:
        _validate_nodes([goal], coords, "Goal")

    if max_frames is not None:

        if max_frames < 2:
            raise ValueError(
                "max_frames must be at least 2"
            )

        if len(events) > max_frames:

            indices = np.linspace(
                0,
                len(events) - 1,
                num=max_frames,
                dtype=int,
            )

            events = [
                events[index]
                for index in indices
            ]

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
                alpha=0.7,
                zorder=1,
            )
        )

    ax.scatter(
        [point[0] for point in coords.values()],
        [point[1] for point in coords.values()],
        s=7,
        c=COLORS["unexplored"],
        alpha=0.7,
        zorder=2,
        label="Locations",
    )

    explored_scatter = ax.scatter(
        np.empty((0, 2)),
        np.empty((0, 2)),
        s=16,
        c=COLORS["explored"],
        label="Explored",
        zorder=3,
    )

    frontier_scatter = ax.scatter(
        np.empty((0, 2)),
        np.empty((0, 2)),
        s=23,
        c=COLORS["frontier"],
        label="Frontier",
        zorder=4,
    )

    path_lines = LineCollection(
        [],
        colors=COLORS["path"],
        linewidths=3.0,
        label="Final path",
        zorder=5,
    )

    ax.add_collection(path_lines)

    if start is not None:
        ax.scatter(
            [coords[start][0]],
            [coords[start][1]],
            s=95,
            c=COLORS["start"],
            label="Start",
            zorder=8,
        )

    if goal is not None:
        ax.scatter(
            [coords[goal][0]],
            [coords[goal][1]],
            s=95,
            c=COLORS["goal"],
            label="Goal",
            zorder=9,
        )

    ax.set_xlabel("X coordinate (km)")
    ax.set_ylabel("Y coordinate (km)")
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(alpha=0.18)
    ax.legend(loc="best", fontsize=8)

    explored_order = []
    explored_set = set()

    def update(frame):

        event = events[frame]
        node = event["node"]

        if node not in explored_set:
            explored_set.add(node)
            explored_order.append(node)

        explored_points = (
            np.array(
                [coords[n] for n in explored_order],
                dtype=float,
            )
            if explored_order
            else np.empty((0, 2))
        )

        visible_frontier = (
            sorted(set(event["frontier"]) - explored_set)
        )

        frontier_points = (
            np.array(
                [coords[n] for n in visible_frontier],
                dtype=float,
            )
            if visible_frontier
            else np.empty((0, 2))
        )

        explored_scatter.set_offsets(explored_points)
        frontier_scatter.set_offsets(frontier_points)

        if frame == len(events) - 1 and len(path) >= 2:

            path_lines.set_segments([
                [coords[u], coords[v]]
                for u, v in zip(path, path[1:])
            ])

        algorithm = result.get("algorithm", "Search")

        ax.set_title(
            f"OptiMap - {algorithm} | "
            f"Step {frame + 1}/{len(events)}"
        )

        return (
            explored_scatter,
            frontier_scatter,
            path_lines,
        )

    animation = FuncAnimation(
        fig,
        update,
        frames=len(events),
        interval=interval,
        repeat=repeat,
        blit=False,
    )

    if save_path is not None:

        output = Path(save_path)
        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        suffix = output.suffix.lower()

        if suffix == ".gif":

            from matplotlib.animation import PillowWriter

            animation.save(
                str(output),
                writer=PillowWriter(
                    fps=max(1, round(1000 / interval))
                ),
            )

        elif suffix == ".mp4":

            animation.save(
                str(output),
                writer="ffmpeg",
                fps=max(1, round(1000 / interval)),
            )

        else:
            raise ValueError(
                "save_path must end with .gif or .mp4"
            )

    if show:
        plt.show()

    return animation, fig, ax
