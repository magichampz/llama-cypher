import json
import matplotlib.pyplot as plt
import numpy as np

def plot_training_loss(json_file_path):
    # Read the JSON file
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    # Extract steps and losses from log_history
    steps = []
    losses = []
    for entry in data['log_history']:
        if 'loss' in entry:
            steps.append(entry['step'])
            losses.append(entry['loss'])
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(steps, losses, 'b-', label='Training Loss')
    plt.xlabel('Steps')
    plt.ylabel('Loss')
    plt.title('Training Loss Over Time')
    plt.grid(True)
    plt.legend()
    
    # Save the plot
    plt.savefig('training_loss_plot.png')
    plt.close()

if __name__ == "__main__":
    plot_training_loss('finetuning-runs/trainer_state-2.json') 