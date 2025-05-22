import json
import random
from openai import OpenAI
from langchain_ollama import ChatOllama
import anthropic
import os
import time
from anthropic._exceptions import OverloadedError

# Initialize API clients
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
claude_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def ask_gpt(question, model_name):
    """Get response from a GPT model"""
    prompt = f"""Please answer the following question concisely in 2-3 sentences:

{question}"""
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return response.choices[0].message.content.strip()

def ask_llama(question, model_name):
    """Get response from a Llama model"""
    prompt = f"""Please answer the following question concisely in 2-3 sentences:

{question}"""
    llama = ChatOllama(
        model=model_name,
        temperature=0.1
        )
    response = llama.invoke(prompt)
    return response.content.strip()

def get_llm_judge_comparison(question, response1, response2, max_retries=3, retry_delay=5):
    """Get Claude's comparison of two model responses with retry logic"""
    prompt = f"""You are an expert judge evaluating the quality of two different AI model responses to a question. 
    Compare the responses and determine which one better answers the question. Consider factors like:
    - Accuracy and correctness
    - Completeness of the answer
    - Clarity and coherence
    - Relevance to the question
    
    Question: {question}
    
    Response 1: {response1}
    
    Response 2: {response2}
    
    Please provide your judgment in the following format:
    WINNER: [1 or 2]
    REASONING: [Your explanation for why one response is better]
    """
    
    for attempt in range(max_retries):
        try:
            response = claude_client.messages.create(
                model="claude-3-5-haiku-latest",
                max_tokens=500,
                temperature=0,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except OverloadedError:
            if attempt < max_retries - 1:
                print(f"Claude API overloaded. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Skipping this comparison.")
                return "WINNER: TIE\nREASONING: Unable to get Claude's judgment due to API overload."
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return "WINNER: TIE\nREASONING: Error occurred during judgment."

def evaluate_models(model1_name, model2_name, model1_type, model2_type, selected_questions, num_questions=50):
    """Evaluate two models using Claude as a judge"""
    # Load questions
    # with open('training_data_2.jsonl', 'r') as f:
    #     all_questions = [json.loads(line) for line in f]
    
    # # Randomly select questions
    # selected_questions = random.sample(all_questions, num_questions)
    
    # Initialize counters
    model1_wins = 0
    model2_wins = 0
    ties = 0
    
    print(f"\nEvaluating {model1_name} vs {model2_name}...")
    print("=" * 80)
    
    for i, q in enumerate(selected_questions, 1):
        question = q['question']
        # print(f"\nQuestion {i}: {question}")
        
        # Get responses from both models
        if model1_type == 'gpt':
            response1 = ask_gpt(question, model1_name)
        else:
            response1 = ask_llama(question, model1_name)
            
        if model2_type == 'gpt':
            response2 = ask_gpt(question, model2_name)
        else:
            response2 = ask_llama(question, model2_name)
            
            
        
        # print(f"\n{model1_name} response: {response1}")
        # print(f"\n{model2_name} response: {response2}")
        
        # Get Claude's judgment
        judgment = get_llm_judge_comparison(question, response1, response2)
        # print(f"\nClaude's judgment:\n{judgment}")
        
        # Parse the judgment
        if "WINNER: 1" in judgment:
            model1_wins += 1
        elif "WINNER: 2" in judgment:
            model2_wins += 1
        else:
            ties += 1
            
        # print("-" * 80)
    
    # Print final results
    print("\nFinal Results:")
    print(f"{model1_name} wins: {model1_wins}")
    print(f"{model2_name} wins: {model2_wins}")
    print(f"Ties: {ties}")
    print(f"\n{model1_name} win rate: {(model1_wins/num_questions)*100:.1f}%")
    print(f"{model2_name} win rate: {(model2_wins/num_questions)*100:.1f}%")
    print("-" * 80)
if __name__ == "__main__":
    # Example usage:
    # evaluate_models("gpt-4.1", "hf.co/unsloth/Llama-3.2-3B-Instruct-GGUF:Q4_K_M", "gpt", "llama")
    # evaluate_models("gpt-4.1", "hf.co/magichampz/llama-3b-tuned-1:Q4_K_M", "gpt", "llama")
    num_questions=50
    
    with open('training_data_2.jsonl', 'r') as f:
        all_questions = [json.loads(line) for line in f]
    
    # Randomly select questions
    selected_questions = random.sample(all_questions, num_questions)
    print("Number of Questions: ", num_questions)
    
    evaluate_models("hf.co/magichampz/llama-3b-tuned-2:Q4_K_M", "hf.co/unsloth/Llama-3.2-3B-Instruct-GGUF:Q4_K_M", "llama", "llama", selected_questions, num_questions)
    evaluate_models("hf.co/magichampz/llama-3b-tuned-1:Q4_K_M", "hf.co/unsloth/Llama-3.2-3B-Instruct-GGUF:Q4_K_M", "llama", "llama", selected_questions, num_questions)
    # pass 