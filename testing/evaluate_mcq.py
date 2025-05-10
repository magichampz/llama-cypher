import json
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
from langchain_ollama import ChatOllama
import os

# Load questions
with open('testing/cybersecurity_mcq.json', 'r') as f:
    questions = json.load(f)

# Set up OpenAI API key (assumes it's in your environment)

# Set up ChatOllama for llama3.2:3b
llama = ChatOllama(model="llama3.2:3b")

def ask_gpt4o(question, options):
    prompt = f"""
Answer the following multiple choice question by giving only the letter of the correct answer (A, B, C, or D):\n\n{question}\nOptions:\n"""
    for letter, text in options.items():
        prompt += f"{letter}. {text}\n"
    prompt += "\nAnswer:"
    response = client.chat.completions.create(model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1,
    temperature=0)
    return response.choices[0].message.content.strip().upper()

def ask_llama(question, options):
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

def evaluate(model_func, model_name):
    correct = 0
    print(f"\nEvaluating {model_name}...\n")
    for i, q in enumerate(questions):
        pred = model_func(q['question'], q['options'])
        is_correct = pred == q['answer']
        print(f"Q{i+1}: {q['question']}\nModel Answer: {pred} | Correct: {q['answer']} | {'✅' if is_correct else '❌'}\n")
        if is_correct:
            correct += 1
    print(f"{model_name} got {correct}/{len(questions)} correct. Accuracy: {correct/len(questions)*100:.1f}%\n")

if __name__ == "__main__":
    # evaluate(ask_gpt4o, "GPT-4o")
    evaluate(ask_llama, "Llama 3.2:3b") 