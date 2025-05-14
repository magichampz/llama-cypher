import json
import os
from openai import OpenAI
from collections import defaultdict


def generate_mcq_pairs(topic, subtopic):
    prompt = f"""
    Topic: {topic}
    Subtopic: {subtopic}
    Generate 4 multiple choice questions (MCQs) about this topic and subtopic in healthcare cybersecurity.
    Each question should have a clear, concise question stem, 4 answer options (A, B, C, D), and one correct answer.

    For each MCQ, output a JSON object with the following fields:
    - 'topic': the topic name
    - 'subtopic': the subtopic name
    - 'question': the question stem
    - 'options': an array of 4 options labeled A, B, C, D (DO NOT include trailing commas after the last option)
    - 'correct_answer': the letter of the correct option (A, B, C, or D)

    Return the entries as a JSON array of 4 objects.
    DO NOT include any markdown code block markers in the response.
    IMPORTANT: Do not include trailing commas in any JSON arrays.
    """
    print(f"\nGenerating MCQs for: {topic} > {subtopic}")
    print("--------------------------------")
    response = client.chat.completions.create(
        model="gpt-4.1",
        temperature=0.7,  # Slightly higher temperature for more diverse questions
        messages=[
            {"role": "system", "content": "You are a cybersecurity expert specialized in healthcare security and medical device security. Focus on generating clear, accurate, and practical multiple choice questions that test understanding of medical cybersecurity concepts. Ensure all JSON output is valid without trailing commas."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def main():
    # Load the dataset
    with open('create-dataset/dataset_keywords.json', 'r') as file:
        dataset = json.load(file)

    # Initialize OpenAI API client
    global client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Initialize statistics tracking
    topic_stats = defaultdict(int)
    subtopic_stats = defaultdict(int)

    # Iterate over topics and subtopics to generate MCQ pairs
    mcq_pairs = []
    for topic in dataset['topics']:
        print(f"\n=== Processing Topic: {topic['name']} ===")
        for subtopic in topic['subtopics']:
            try:
                mcq_content = generate_mcq_pairs(topic['name'], subtopic['name'])
                # Parse the JSON response
                mcq_entries = json.loads(mcq_content)
                
                # Print the generated MCQs in a nicely formatted way
                # print("\nGenerated MCQs:")
                # print(json.dumps(mcq_entries, indent=2))
                # print("--------------------------------")
                
                # Add each MCQ entry to our collection
                for entry in mcq_entries:
                    mcq_pairs.append(entry)
                    # Update statistics
                    topic_stats[topic['name']] += 1
                    subtopic_stats[f"{topic['name']} > {subtopic['name']}"] += 1
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON for {topic['name']} > {subtopic['name']}: {e}")
                print(f"Raw content: {mcq_content}")
            except Exception as e:
                print(f"Error processing {topic['name']} > {subtopic['name']}: {e}")

    # Save the MCQ pairs to a JSONL file
    with open('mcq_evaluation.jsonl', 'w') as outfile:
        for mcq_pair in mcq_pairs:
            json.dump(mcq_pair, outfile)
            outfile.write('\n')

    # Print statistics
    print("\n=== Generation Statistics ===")
    print(f"\nTotal MCQs generated: {len(mcq_pairs)}")

    print("\nBy Topic:")
    for topic, count in topic_stats.items():
        print(f"- {topic}: {count} MCQs")

    # print("\nBy Subtopic:")
    # for subtopic, count in subtopic_stats.items():
    #     print(f"- {subtopic}: {count} MCQs")

if __name__ == '__main__':
    main() 