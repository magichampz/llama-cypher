import json
import sys

def jsonl_to_json(jsonl_file, json_file):
    # Read JSONL file and convert to list of objects
    objects = []
    with open(jsonl_file, 'r') as f:
        for line in f:
            if line.strip():  # Skip empty lines
                objects.append(json.loads(line))
    
    # Write to JSON file
    with open(json_file, 'w') as f:
        json.dump(objects, f, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python jsonl_to_json.py input.jsonl output.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        jsonl_to_json(input_file, output_file)
        print(f"Successfully converted {input_file} to {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1) 