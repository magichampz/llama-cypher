from datasets import Dataset
import json
from huggingface_hub import HfApi
import os
from datetime import datetime

def load_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def create_readme(dataset):
    # Count unique topics and subtopics
    topics = set()
    subtopics = set()
    for item in dataset:
        topics.add(item['topic'])
        subtopics.add(f"{item['topic']} > {item['subtopic']}")
    
    readme_content = f"""---
language:
- en
license:
- mit
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- question-answering
---

# Medical Cybersecurity Q&A Dataset

This dataset contains question-answer pairs focused on medical device cybersecurity and healthcare security.

## Dataset Information
- Total Q&A pairs: {len(dataset)}
- Number of unique topics: {len(topics)}
- Number of unique subtopics: {len(subtopics)}
- Last updated: {datetime.now().strftime('%Y-%m-%d')}

## Topics Covered
{chr(10).join(f"- {topic}" for topic in sorted(topics))}

## Data Format
Each entry contains:
- topic: The main topic category
- subtopic: The specific subtopic within the main topic
- keyword: The specific keyword being addressed
- question: A question about the keyword in the context of the topic
- answer: A detailed answer to the question

## Usage
This dataset can be used for training models to understand and generate responses about medical cybersecurity topics.
"""
    return readme_content

def main():
    # Load the JSONL file
    data = load_jsonl('val.jsonl')
    
    
    # Convert to Hugging Face dataset
    dataset = Dataset.from_list(data)
    
    # Get token from environment variable
    token = os.getenv('HUGGINGFACE_TOKEN')
    if not token:
        raise ValueError("Please set the HUGGINGFACE_TOKEN environment variable")
    
    # Initialize Hugging Face API with token
    api = HfApi(token=token)
    
    # Create a new dataset repository
    repo_name = "magichampz/medical-cyber-val"
    
    # Create README content
    readme_content = create_readme(data)
    
    # Push the dataset to Hugging Face with commit message
    commit_message = f"Update dataset with {len(data)} Q&A pairs - {datetime.now().strftime('%Y-%m-%d')}"
    dataset.push_to_hub(
        repo_name,
        commit_message=commit_message,
        commit_description="Adding new Q&A pairs and updating README with latest statistics"
    )
    
    # Update README
    api.upload_file(
        path_or_fileobj=readme_content.encode(),
        path_in_repo="README.md",
        repo_id=repo_name,
        repo_type="dataset",
        commit_message="Update README with latest dataset statistics"
    )

if __name__ == "__main__":
    main() 