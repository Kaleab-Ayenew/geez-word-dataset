#!/usr/bin/env python3
"""
Add one or more fields to all JSON objects in all JSON files in a directory.
Defaults to adding 'amharic_meaning' if no field names are given.
New fields are set to empty string "" if not already present.
"""

import json
import sys
from pathlib import Path

# Default fields to add when none specified
DEFAULT_FIELDS = ["amharic_meaning"]


def add_fields_to_objects(directory_path: str, field_names: list[str]) -> None:
    """
    Add the given fields to all JSON objects in all JSON files in the directory.
    Only adds a field if it does not already exist (does not overwrite).

    Args:
        directory_path: Path to the directory containing JSON files
        field_names: List of field names to add (each with default value "")
    """
    directory = Path(directory_path)

    if not directory.exists():
        print(f"Error: Directory '{directory_path}' does not exist.")
        sys.exit(1)

    if not directory.is_dir():
        print(f"Error: '{directory_path}' is not a directory.")
        sys.exit(1)

    if not field_names:
        field_names = DEFAULT_FIELDS.copy()

    json_files = list(directory.glob("*.json"))
    if not json_files:
        print(f"No JSON files found in '{directory_path}'")
        return

    print(f"Adding field(s): {', '.join(field_names)}")
    print(f"Found {len(json_files)} JSON files in '{directory_path}'")

    modified_count = 0
    error_count = 0

    for json_file in sorted(json_files):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, list):
                print(f"  Warning: {json_file.name} does not contain a list. Skipping.")
                continue

            objects_modified = 0
            for obj in data:
                if isinstance(obj, dict):
                    for field in field_names:
                        if field not in obj:
                            obj[field] = ""
                            objects_modified += 1

            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            if objects_modified:
                print(f"  ✓ {json_file.name}: added {objects_modified} field(s)")
            modified_count += 1

        except json.JSONDecodeError as e:
            print(f"  ✗ Error parsing JSON in {json_file.name}: {e}")
            error_count += 1
        except Exception as e:
            print(f"  ✗ Error processing {json_file.name}: {e}")
            error_count += 1

    print(f"\n{'='*60}")
    print("Summary:")
    print(f"  Total files: {len(json_files)}")
    print(f"  Processed:   {modified_count}")
    print(f"  Errors:      {error_count}")
    print(f"{'='*60}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python add_fields.py <directory> [field1 [field2 ...]]")
        print("\n  Adds the given fields (default: amharic_meaning) to every object in every JSON file.")
        print("  New fields get value \"\". Existing fields are left unchanged.")
        print("\nExamples:")
        print("  python add_fields.py .")
        print("  python add_fields.py . amharic_meaning")
        print("  python add_fields.py /path/to/jsons amharic_meaning tigrinya_meaning")
        sys.exit(1)

    directory_path = sys.argv[1]
    field_names = sys.argv[2:] if len(sys.argv) > 2 else DEFAULT_FIELDS.copy()
    add_fields_to_objects(directory_path, field_names)


if __name__ == "__main__":
    main()
