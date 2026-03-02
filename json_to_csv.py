#!/usr/bin/env python3
"""
Convert all JSON files in the current directory to CSV.
Uses the JSON object keys as CSV column headers.
Handles Unicode (e.g. Ge'ez) and fields containing commas/newlines.
"""

import csv
import json
import os
from pathlib import Path


def json_to_csv(json_path: Path, csv_path: Path) -> None:
    """Convert a single JSON file (array of objects) to CSV."""
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(f"Expected JSON array, got {type(data).__name__}")

    if not data:
        # Empty array: write CSV with no data rows (no columns known)
        csv_path.write_text("", encoding="utf-8")
        return

    # Use first object's keys as column order; ensure consistent across all rows
    fieldnames = list(data[0].keys())

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_MINIMAL,
            extrasaction="ignore",
        )
        writer.writeheader()
        for row in data:
            # Normalize: ensure all keys exist, fill missing with ""
            normalized = {k: row.get(k, "") for k in fieldnames}
            # Coerce values to str for CSV
            normalized = {k: (v if v is not None else "") for k, v in normalized.items()}
            writer.writerow(normalized)


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    json_files = sorted(script_dir.glob("*.json"))

    if not json_files:
        print("No .json files found in", script_dir)
        return
    json_files = [Path("ሀ copy.json")]
    for json_path in json_files:
        csv_path = json_path.with_suffix(".csv")
        try:
            json_to_csv(json_path, csv_path)
            print(f"  {json_path.name}  ->  {csv_path.name}")
        except Exception as e:
            print(f"  ERROR {json_path.name}: {e}")

    print(f"\nDone. Converted {len(json_files)} file(s).")


if __name__ == "__main__":
    main()
