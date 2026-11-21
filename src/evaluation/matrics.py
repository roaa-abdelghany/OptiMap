import csv
from pathlib import Path

FIELDS = ["algorithm", "found", "path_cost", "nodes_generated", "nodes_expanded",
          "max_frontier_size", "running_time", "path"]

def export_results(results, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for r in results:
            row = dict(r)
            row["path"] = " -> ".join(row.get("path", []))
            writer.writerow({k: row.get(k) for k in FIELDS})
