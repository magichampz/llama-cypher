import json
import os
from openai import OpenAI
from collections import defaultdict
from prompts import MCQ_GENERATION_PROMPT_2, SYSTEM_MESSAGE, question_focuses

def generate_mcq(topic, subtopic, question_focus):
    prompt = MCQ_GENERATION_PROMPT_2.format(
        topic=topic,
        subtopic=subtopic,
        question_focus=question_focus
    )
    # print(f"\nGenerating MCQ for: {topic} > {subtopic}")
    print(f"Question Focus: {question_focus}")
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
        # Fix common JSON formatting issues
        content = content.replace("\\'", "'")  # Remove unnecessary single quote escaping
        
        # Try to parse the JSON
        data = json.loads(content)
        
        # Validate structure
        if not isinstance(data, dict):
            raise ValueError("Response must be a JSON object")
            
        required_fields = ['topic', 'subtopic', 'question', 'options', 'correct_answer']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate options array
        if not isinstance(data['options'], list) or len(data['options']) != 4:
            raise ValueError("Options must be an array with exactly 4 items")
        
        # Validate correct_answer
        if data['correct_answer'] not in ['A', 'B', 'C', 'D']:
            raise ValueError("Correct answer must be A, B, C, or D")
        
        # Validate string content
        for field in ['topic', 'subtopic', 'question']:
            if not isinstance(data[field], str):
                raise ValueError(f"Field '{field}' must be a string")
            if '\n' in data[field]:
                raise ValueError(f"Field '{field}' contains newlines")
        
        for option in data['options']:
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
    focus_stats = defaultdict(int)

    # Iterate over topics and subtopics to generate MCQs
    mcqs = []
    for topic in dataset['topics']:
        print(f"\n=== Processing Topic: {topic['name']} ===")
        for subtopic in topic['subtopics']:
            print(f"\nGenerating MCQ for: {topic['name']} > {subtopic['name']}")
            for focus in question_focuses:
                try:
                    mcq_content = generate_mcq(topic['name'], subtopic['name'], focus)
                    
                    # Validate the response before parsing
                    if not validate_json_response(mcq_content):
                        print(f"Skipping invalid response for {topic['name']} > {subtopic['name']} > {focus}")
                        continue
                    
                    # Parse the JSON response
                    mcq_entry = json.loads(mcq_content)
                    
                    # Add the MCQ entry to our collection
                    mcqs.append(mcq_entry)
                    
                    # Update statistics
                    topic_stats[topic['name']] += 1
                    subtopic_stats[f"{topic['name']} > {subtopic['name']}"] += 1
                    focus_stats[focus] += 1
                    
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON for {topic['name']} > {subtopic['name']} > {focus}: {e}")
                    print(f"Raw content: {mcq_content}")
                except Exception as e:
                    print(f"Error processing {topic['name']} > {subtopic['name']} > {focus}: {e}")

    # Save the MCQs to a JSONL file
    with open('mcq_evaluation_new_1.jsonl', 'w') as outfile:
        for mcq in mcqs:
            json.dump(mcq, outfile)
            outfile.write('\n')

    # Print statistics
    print("\n=== Generation Statistics ===")
    print(f"\nTotal MCQs generated: {len(mcqs)}")

    print("\nBy Topic:")
    for topic, count in topic_stats.items():
        print(f"- {topic}: {count} MCQs")

    # print("\nBy Subtopic:")
    # for subtopic, count in subtopic_stats.items():
    #     print(f"- {subtopic}: {count} MCQs")
        
    # print("\nBy Question Focus:")
    # for focus, count in focus_stats.items():
    #     print(f"- {focus}: {count} MCQs")

if __name__ == '__main__':
    main() 