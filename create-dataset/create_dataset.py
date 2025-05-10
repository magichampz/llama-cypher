import json
from openai import OpenAI
import os
from typing import List, Dict, Optional

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_training_data(
    category: str,
    num_entries: int = 5,
    specific_focus: Optional[str] = None,
) -> List[Dict]:
    """
    Generate training data using GPT-4o that focuses on deep understanding and reasoning.
    
    Args:
        category: Main category for the training data
        num_entries: Number of training entries to generate
        specific_focus: Optional specific focus area within the category
    
    Returns:
        List of training data dictionaries
    """
    prompt = f"""
    Generate {num_entries} training entries about {category}. 
    The purpose of the training data is to train a small model to get 
    better at answering questions related to cybersecurity in healthcare."""
    
    prompt += f" Specific focus: {specific_focus}.\n\n"
    prompt += """Each entry should be in the following format:

{
    "category": "string",
    "question": "string",
    "answer": "string (detailed explanation with concepts involved)",
}


DO NOT include any markdown code block markers in the response.
Requirements:
1. The dataset should focus on teaching concepts deeply and explicitly with context, explanations and reasoning.
2. We want the smaller model to "internalize" cybersecurity knoweldge.
2. Focus on deep understanding and reasoning
3. Include real-world examples and scenarios
4. Explain security concepts thoroughly
6. Highlight key concepts and lessons learned
9. Ensure accuracy and technical correctness

Return the entries as a JSON array."""

    # Call GPT-4o
    print(prompt)
    print("-"*100)
    print("Generating training data...")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=4000
    )

    # Extract and parse the JSON response
    try:
        training_data = json.loads(response.choices[0].message.content)
        return training_data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print("Raw response:", response.choices[0].message.content)
        return []

def save_training_data(
    training_data: List[Dict],
    output_file: str,
) -> None:
    """
    Save generated training data to a JSON file. If the file exists, append the data.
    If the file doesn't exist, create it with the data as the first entries.
    
    Args:
        training_data: List of training data dictionaries
        output_file: Path to output JSON file
    """
    try:
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                existing_data = json.load(f)
            all_data = existing_data + training_data
        else:
            all_data = training_data

        with open(output_file, 'w') as f:
            json.dump(all_data, f, indent=2)
            
        print(f"Successfully saved {len(training_data)} entries to {output_file}")
    except Exception as e:
        print(f"Error saving training data: {e}")

def main():
    # Example usage
    training_data = generate_training_data(
        category="Medical Device Security",
        num_entries=1,
        specific_focus="Understanding physical and network-based attack vectors in healthcare environments, including device vulnerabilities, supply chain risks, and security best practices"
    )
    
    # Print the generated training data
    print("\nGenerated Training Data:")
    print(json.dumps(training_data, indent=2))
    
    output_file = "create-dataset/training_data.json"
    # Ask user if they want to save the data
    save = input("\nDo you want to save this training data? (y/n): ").lower()
    if save == 'y':
        save_training_data(training_data, output_file=output_file)

if __name__ == "__main__":
    main() 