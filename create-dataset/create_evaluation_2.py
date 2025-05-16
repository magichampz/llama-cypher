import json
import os
from openai import OpenAI
from collections import defaultdict
from prompts import MCQ_GENERATION_PROMPT_1, SYSTEM_MESSAGE


def generate_mcq_pairs(topic, subtopic):
    prompt = MCQ_GENERATION_PROMPT_1.format(topic=topic, subtopic=subtopic)
    print(f"\nGenerating MCQs for: {topic} > {subtopic}")
    print("--------------------------------")
    response = client.chat.completions.create(
        model="gpt-4.1",
        temperature=0.7,  # Slightly higher temperature for more diverse questions
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def validate_json_response(content):
    try:
        # Try to parse the JSON
        data = json.loads(content)
        
        # Validate structure
        if not isinstance(data, list):
            raise ValueError("Response must be a JSON array")
            
        for item in data:
            required_fields = ['topic', 'subtopic', 'question', 'options', 'correct_answer']
            for field in required_fields:
                if field not in item:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate options array
            if not isinstance(item['options'], list) or len(item['options']) != 4:
                raise ValueError("Options must be an array with exactly 4 items")
            
            # Validate correct_answer
            if item['correct_answer'] not in ['A', 'B', 'C', 'D']:
                raise ValueError("Correct answer must be A, B, C, or D")
            
            # Validate string content
            for field in ['topic', 'subtopic', 'question']:
                if not isinstance(item[field], str):
                    raise ValueError(f"Field '{field}' must be a string")
                if '\n' in item[field]:
                    raise ValueError(f"Field '{field}' contains newlines")
            
            for option in item['options']:
                if not isinstance(option, str):
                    raise ValueError("All options must be strings")
                if '\n' in option:
                    raise ValueError("Options cannot contain newlines")
        
        return True
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print("Raw content:")
        print(content)
        return False
    except ValueError as e:
        print(f"Validation error: {e}")
        return False

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
    for topic in dataset['topics'][:1]:
        print(f"\n=== Processing Topic: {topic['name']} ===")
        for subtopic in topic['subtopics'][:1]:
            try:
                mcq_content = generate_mcq_pairs(topic['name'], subtopic['name'])
                
                # Validate the response before parsing
                if not validate_json_response(mcq_content):
                    print(f"Skipping invalid response for {topic['name']} > {subtopic['name']}")
                    continue
                
                # Parse the JSON response
                mcq_entries = json.loads(mcq_content)
                
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
    with open('mcq_evaluation_5.jsonl', 'w') as outfile:
        for mcq_pair in mcq_pairs:
            json.dump(mcq_pair, outfile)
            outfile.write('\n')

    # Print statistics
    print("\n=== Generation Statistics ===")
    print(f"\nTotal MCQs generated: {len(mcq_pairs)}")

    print("\nBy Topic:")
    for topic, count in topic_stats.items():
        print(f"- {topic}: {count} MCQs")

    print("\nBy Subtopic:")
    for subtopic, count in subtopic_stats.items():
        print(f"- {subtopic}: {count} MCQs")

if __name__ == '__main__':
    main() 