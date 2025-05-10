import json
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
from langchain_ollama import ChatOllama
import os

# Load questions


# Set up OpenAI API key (assumes it's in your environment)

# Set up ChatOllama for llama3.2:3b

def ask_gpt4o(question, options, model_name):
    prompt = f"""
Answer the following multiple choice question by giving only the letter of the correct answer (A, B, C, or D):\n\n{question}\nOptions:\n"""
    for letter, text in options.items():
        prompt += f"{letter}. {text}\n"
    prompt += "\nAnswer:"
    response = client.chat.completions.create(model=model_name,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1,
    temperature=0)
    return response.choices[0].message.content.strip().upper()

def ask_llama(question, options, model_name):
    llama = ChatOllama(model=model_name)
    
    prompt = f"""
Answer the following multiple choice question by giving only the letter of the correct answer (A, B, C, or D):\n\n{question}\nOptions:\n"""
    for letter, text in options.items():
        prompt += f"{letter}. {text}\n"
    prompt += "\nAnswer:"
    response = llama.invoke(prompt)
    # print("response is: ",response.content)
    # Extract the first letter A-D from the response
    # for letter in ['A', 'B', 'C', 'D']:
    #     if letter in response:
    #         return letter
    return response.content.strip()[0].upper()

def evaluate(model_func, model_name, questions):
    correct = 0
    print(f"\nEvaluating {model_name}...\n")
    for i, q in enumerate(questions):
        pred = model_func(q['question'], q['options'], model_name)
        is_correct = pred == q['answer']
        print(f"Q{i+1}: {q['question']}\nModel Answer: {pred} | Correct: {q['answer']} | {'✅' if is_correct else '❌'}\n")
        if is_correct:
            correct += 1
    print(f"{model_name} got {correct}/{len(questions)} correct. Accuracy: {correct/len(questions)*100:.1f}%\n")

if __name__ == "__main__":
    test_file = "create-dataset/evaluation_data.json"
    with open(test_file, 'r') as f:
        questions = json.load(f)
    # evaluate(ask_gpt4o, "gpt-4o", questions)
    # evaluate(ask_llama, "llama3.2:3b", questions) 
    evaluate(ask_llama, "llama3.2:1b", questions) 
    # evaluate(ask_llama, "llama3.1:8b", questions) 
    # evaluate(ask_llama, "unsloth8bi", questions) 
    