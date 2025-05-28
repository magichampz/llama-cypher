import json
import random

# Set random seed for reproducibility
random.seed(42)

# Read the JSONL file
with open('training_data_2.jsonl', 'r') as f:
    data = [json.loads(line) for line in f]

# Shuffle the data
random.shuffle(data)

# Calculate split sizes
total_size = len(data)
train_size = int(0.7 * total_size)
val_size = int(0.15 * total_size)
test_size = total_size - train_size - val_size

# Split the data
train_data = data[:train_size]
val_data = data[train_size:train_size + val_size]
test_data = data[train_size + val_size:]

# Write the splits to separate files
def write_jsonl(data, filename):
    with open(filename, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')

write_jsonl(train_data, 'train.jsonl')
write_jsonl(val_data, 'val.jsonl')
write_jsonl(test_data, 'test.jsonl')

# Print statistics
print(f"Total examples: {total_size}")
print(f"Train set size: {len(train_data)} ({len(train_data)/total_size:.1%})")
print(f"Validation set size: {len(val_data)} ({len(val_data)/total_size:.1%})")
print(f"Test set size: {len(test_data)} ({len(test_data)/total_size:.1%})") 