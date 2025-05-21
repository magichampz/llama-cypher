import json
import os
from openai import OpenAI
from collections import defaultdict

def analyze_dataset_structure(dataset):
    print("\n=== Dataset Structure Analysis ===")
    
    # Count topics and subtopics
    num_topics = len(dataset['topics'])
    total_subtopics = sum(len(topic['subtopics']) for topic in dataset['topics'])
    total_keywords = sum(len(subtopic['keywords']) for topic in dataset['topics'] for subtopic in topic['subtopics'])
    
    print(f"\nTotal Counts:")
    print(f"  Topics: {num_topics}")
    print(f"  Subtopics: {total_subtopics}")
    print(f"  Keywords: {total_keywords}")
    
    # Analyze each topic
    for topic in dataset['topics']:
        num_subtopics = len(topic['subtopics'])
        topic_keywords = sum(len(subtopic['keywords']) for subtopic in topic['subtopics'])
        
        print(f"\nTopic: {topic['name']}")
        print(f"  Number of Subtopics: {num_subtopics}")
        print(f"  Total Keywords: {topic_keywords}")
        
        # Show subtopic breakdown
        for subtopic in topic['subtopics']:
            print(f"  - {subtopic['name']}: {len(subtopic['keywords'])} keywords")

def generate_qa_pairs(topic, subtopic, keyword):
    prompt = f"""
Topic: {topic}
Subtopic: {subtopic}
Generate 2 questions about {keyword} in the context of the given topic and subtopic.
For each question, provide a detailed and well-explained answer that is accurate, practical, and relevant.
For each data entry, output a JSON object with the following fields- 'topic': {topic}, 'subtopic': {subtopic}, 'keyword': {keyword}, 'question' and 'answer'.
Return the entries as a JSON array. 
DO NOT include any markdown code block markers in the response.
    """
    print(f"Generating Q&A for: {keyword}")
    # print(prompt)
    print("--------------------------------")
    response = client.chat.completions.create(
        # model="gpt-4o",
        model="gpt-4.1",
        temperature=0.3,  # Lower temperature for more consistent, focused outputs
        messages=[
            {"role": "system", "content": "You are a cybersecurity expert specialized in healthcare security and medical device security. Focus on generating clear, accurate, and practical questions that test understanding of medical cybersecurity concepts."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def main():
    # Load the dataset
    with open('create-dataset/dataset_keywords.json', 'r') as file:
        dataset = json.load(file)

    # Analyze the dataset structure
    # analyze_dataset_structure(dataset)

    # Initialize OpenAI API client
    global client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Initialize statistics tracking
    topic_stats = defaultdict(int)
    subtopic_stats = defaultdict(int)
    keyword_stats = defaultdict(int)

    # Iterate over topics, subtopics, and keywords to generate Q&A pairs
    qa_pairs = []
    for topic in dataset['topics']:
        for subtopic in topic['subtopics']:
            print(f"Topic: {topic['name']}\nSubtopic: {subtopic['name']}")
            for keyword in subtopic['keywords']:
                try:
                    # print(f"Generating Q&A for: {keyword}")
                    qa_content = generate_qa_pairs(topic['name'], subtopic['name'], keyword)
                    # Parse the JSON response
                    qa_entries = json.loads(qa_content)
                    
                    # Add each Q&A entry as a separate object with topic, subtopic, and keyword info
                    for entry in qa_entries:
                        # print(entry)
                        qa_pairs.append({
                            "topic": topic['name'],
                            "subtopic": subtopic['name'],
                            "keyword": keyword,
                            "question": entry['question'],
                            "answer": entry['answer']
                        })
                        # Update statistics
                        topic_stats[topic['name']] += 1
                        subtopic_stats[f"{topic['name']} > {subtopic['name']}"] += 1
                        keyword_stats[f"{topic['name']} > {subtopic['name']} > {keyword}"] += 1
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON for {keyword}: {e}")
                    print(f"Raw content: {qa_content}")
                except Exception as e:
                    print(f"Error processing {keyword}: {e}")

    # Save the Q&A pairs to a JSONL file
    with open('training_data_2.jsonl', 'w') as outfile:
        for qa_pair in qa_pairs:
            json.dump(qa_pair, outfile)
            outfile.write('\n')
            
    # Save the Q&A pairs to a JSON file
    with open('training_data_2.json', 'w') as outfile:
        json.dump(qa_pairs, outfile, indent=2)

    # Print statistics
    print("\n=== Generation Statistics ===")
    print(f"\nTotal Q&A pairs generated: {len(qa_pairs)}")

    print("\nBy Topic:")
    for topic, count in topic_stats.items():
        print(f"- {topic}: {count} Q&A pairs")

    # print("\nBy Subtopic:")
    # for subtopic, count in subtopic_stats.items():
    #     print(f"- {subtopic}: {count} Q&A pairs")

    # print("\nBy Keyword:")
    # for keyword, count in keyword_stats.items():
    #     print(f"- {keyword}: {count} Q&A pairs")

if __name__ == '__main__':
    main()
    
    # with open('create-dataset/dataset_keywords.json', 'r') as file:
    #     dataset = json.load(file)

    # # Analyze the dataset structure
    # analyze_dataset_structure(dataset)
