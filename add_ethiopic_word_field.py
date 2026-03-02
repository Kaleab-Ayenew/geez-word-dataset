#!/usr/bin/env python3
"""
Script to add 'ethiopic_word' field to all JSON objects in all JSON files in a directory.
"""

import json
import os
import sys
from pathlib import Path


def add_ethiopic_word_field(directory_path):
    """
    Add 'ethiopic_word' field to all JSON objects in all JSON files in the given directory.
    
    Args:
        directory_path: Path to the directory containing JSON files
    """
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"Error: Directory '{directory_path}' does not exist.")
        sys.exit(1)
    
    if not directory.is_dir():
        print(f"Error: '{directory_path}' is not a directory.")
        sys.exit(1)
    
    # Find all JSON files in the directory
    json_files = list(directory.glob("*.json"))
    
    if not json_files:
        print(f"No JSON files found in '{directory_path}'")
        return
    
    print(f"Found {len(json_files)} JSON files in '{directory_path}'")
    
    modified_count = 0
    error_count = 0
    
    for json_file in json_files:
        try:
            print(f"\nProcessing: {json_file.name}")
            
            # Read the JSON file
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if data is a list
            if not isinstance(data, list):
                print(f"  Warning: {json_file.name} does not contain a list. Skipping.")
                continue
            
            # Add 'ethiopic_word' field to each object
            objects_modified = 0
            for obj in data:
                if isinstance(obj, dict):
                    # Only add the field if it doesn't already exist
                    if 'ethiopic_word' not in obj:
                        obj['ethiopic_word'] = ""
                        objects_modified += 1
            
            # Write the modified data back to the file
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            print(f"  ✓ Modified {objects_modified} objects in {json_file.name}")
            modified_count += 1
            
        except json.JSONDecodeError as e:
            print(f"  ✗ Error parsing JSON in {json_file.name}: {e}")
            error_count += 1
        except Exception as e:
            print(f"  ✗ Error processing {json_file.name}: {e}")
            error_count += 1
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total files found: {len(json_files)}")
    print(f"  Successfully modified: {modified_count}")
    print(f"  Errors: {error_count}")
    print(f"{'='*60}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python add_ethiopic_word_field.py <directory_path>")
        print("\nExample: python add_ethiopic_word_field.py /path/to/json/files")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    add_ethiopic_word_field(directory_path)


if __name__ == "__main__":
    main()
