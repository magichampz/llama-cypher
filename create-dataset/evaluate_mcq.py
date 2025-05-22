import json
from openai import OpenAI
import os
from langchain_ollama import ChatOllama
import anthropic

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
claude_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def ask_gpt(question, options, model_name):
    prompt = f"""
Answer the following multiple choice question by giving only the letter of the correct answer (A, B, C, or D):\n\n{question}\nOptions:\n"""
    for option in options:
        prompt += f"{option}\n"
    prompt += "\nAnswer:"
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1,
        temperature=0
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content.strip().upper()

def ask_llama(question, options, model_name):
    llama = ChatOllama(
        model=model_name,
        temperature=0,
        )
    
    prompt = f"""
Answer the following multiple choice question by giving only the letter of the correct answer (A, B, C, or D):\n\n{question}\nOptions:\n"""
    for option in options:
        prompt += f"{option}\n"
    prompt += "\nAnswer:"
    response = llama.invoke(prompt)
    # print(response.content)
    # print()
    return response.content.strip()[0].upper()

def ask_claude(question, options, model_name):
    prompt = f"""
Answer the following multiple choice question by giving only the letter of the correct answer (A, B, C, or D):\n\n{question}\nOptions:\n"""
    for option in options:
        prompt += f"{option}\n"
    prompt += "\nAnswer:"
    
    response = claude_client.messages.create(
        model=model_name,
        max_tokens=1,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    print(response.content[0].text)
    return response.content[0].text.strip().upper()

def evaluate(model_func, model_name, questions):
    correct = 0
    total = len(questions)
    print(f"\n=== Evaluating {model_name}... ===\n")
    
    # Track performance by topic and subtopic
    topic_stats = {}
    subtopic_stats = {}
    
    for i, q in enumerate(questions):
        pred = model_func(q['question'], q['options'], model_name)
        is_correct = pred == q['correct_answer']
        
        # Update topic stats
        topic = q['topic']
        if topic not in topic_stats:
            topic_stats[topic] = {'correct': 0, 'total': 0}
        topic_stats[topic]['total'] += 1
        if is_correct:
            topic_stats[topic]['correct'] += 1
            
        # Update subtopic stats
        subtopic = f"{topic} > {q['subtopic']}"
        if subtopic not in subtopic_stats:
            subtopic_stats[subtopic] = {'correct': 0, 'total': 0}
        subtopic_stats[subtopic]['total'] += 1
        if is_correct:
            subtopic_stats[subtopic]['correct'] += 1
        
        # print(f"Q{i+1}: {q['question']}")
        # print(f"Model Answer: {pred} | Correct: {q['correct_answer']} | {'✅' if is_correct else '❌'}")
        # print(f"Topic: {topic} | Subtopic: {q['subtopic']}\n")
        
        if is_correct:
            correct += 1
    
    
    
    # # Print topic-wise statistics
    # print("\n=== Performance by Topic ===")
    # for topic, stats in topic_stats.items():
    #     accuracy = stats['correct'] / stats['total'] * 100
    #     print(f"{topic}: {stats['correct']}/{stats['total']} correct ({accuracy:.1f}%)")
    
    # # Print subtopic-wise statistics
    # print("\n=== Performance by Subtopic ===")
    # for subtopic, stats in subtopic_stats.items():
    #     accuracy = stats['correct'] / stats['total'] * 100
    #     print(f"{subtopic}: {stats['correct']}/{stats['total']} correct ({accuracy:.1f}%)")
    
    # Print overall statistics
    # print(f"\n=== Overall Performance ===")
    print(f"{model_name} got {correct}/{total} correct. Accuracy: {correct/total*100:.1f}%\n")

def load_questions(file_path):
    questions = []
    with open(file_path, 'r') as f:
        for line in f:
            questions.append(json.loads(line))
    return questions

if __name__ == "__main__":
    # Load questions from the JSONL file
    questions = load_questions('mcq_evaluation_new_1.jsonl')
    
    # Uncomment the models you want to evaluate
    
    # evaluate(ask_gpt, "gpt-4.1", questions) # 192/192 (1), 191/192 (2), 156/159 (3)
    # evaluate(ask_claude, "claude-3-5-haiku-latest", questions)
    
    # evaluate(ask_llama, "llama3.1:8b", questions) # 182/192 (1), 180/192 (2)
    # evaluate(ask_llama, "llama3.2:3b", questions) # 173/192(1), 171/192(2)
    # evaluate(ask_llama, "llama3.2:1b", questions) # 108/192 (1)
    
    # evaluate(ask_llama, "unsloth8bi", questions)
    # evaluate(ask_llama, "llama3b-instruct-og", questions)
    # evaluate(ask_llama, "llama1b-instruct-og", questions)
    
    # evaluate(ask_llama, "llama3b-tuned-1", questions)
    
    
    # comparing base models vs tuned models
    # llama 3.2 3b base
    evaluate(ask_llama, "hf.co/unsloth/Llama-3.2-3B-Instruct-GGUF:Q4_K_M", questions)
    
    # llama 3.2 3b tuned v1
    evaluate(ask_llama, "hf.co/magichampz/llama-3b-tuned-1:Q4_K_M", questions)
    
    # llama 3.2 3b tuned v2
    evaluate(ask_llama, "hf.co/magichampz/llama-3b-tuned-2:Q4_K_M", questions)
    
    
    
    
    