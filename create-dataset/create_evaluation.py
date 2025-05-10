import json
from openai import OpenAI
import os
from typing import List, Dict, Optional
import time

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

general_categories = {
        "Vulnerabilities and Exploits": "Explores weaknesses in medical devices that can be exploited by cyber threats. Inlcude quesitons to aid in understanding of CVEs, but do not hallucinate any CVE IDs.",
        "Bluetooth and Wireless Security": "Covers security measures and vulnerabilities related to Bluetooth and wireless technologies.",
        "Penetration Testing Workflows": "Describes the processes and methodologies used in penetration testing.",
        "Penetration Testing Lifecycle": "Details the stages involved in the lifecycle of penetration testing.",
        "Physical Attack Vectors": "Focuses on physical methods used to compromise security systems.",
        "Network and Application Exploits": "Examines vulnerabilities in networks and applications that can be exploited.",
        "Mitigation and Hardening": "Discusses strategies to strengthen systems against attacks and reduce vulnerabilities. Best practices for device-level, network-level, and application-level security",
        "Incident Response": "Covers the procedures and actions taken in response to security incidents.",
        "Compliance and Legal (HIPAA, MHRA, GDPR)": "Addresses legal and compliance requirements in cybersecurity, as well as Privacy and Data Protection.",
    }

security_tools_categories = {
        "Tool Identification and Purpose": "Questions that ask about the primary use or purpose of a specific tool in Kali Linux, helping the learner understand what each tool is designed to do.",
        "Basic Usage and Commands": "Questions focused on how to use a tool, including its syntax, common command structures, and important flags relevant for penetration testing tasks.",
        "Scenario-Based Tool Selection": "Questions that present a cybersecurity scenario and ask which Kali Linux tool would be most appropriate to use in that context, training the model to map problems to tools.",
        "Command Interpretation": "Questions that provide a specific tool command and ask for an explanation of what the command does, reinforcing understanding of tool functionality and options.",
        "Tool Features and Strengths": "Questions that highlight the key features, strengths, or advantages of a particular tool, helping users compare tools and understand when they excel.",
        "Tool Limitations and Risks": "Questions that discuss the limitations, risks, or considerations when using specific tools, particularly in sensitive environments like healthcare systems.",
        # "Compliance and Legal Considerations": "Questions covering the legal and ethical requirements when using penetration testing tools, emphasizing safe and authorized use of tools in real-world settings.",
    }

def generate_questions(
    category: str,
    num_questions: int = 5,
    difficulty: str = "intermediate",
    description: Optional[str] = None,
) -> List[Dict]:
    """
    Generate cybersecurity questions using GPT-4o.
    
    Args:
        category: Main category for questions (e.g., "General Cybersecurity", "Penetration Testing")
        num_questions: Number of questions to generate
        difficulty: Question difficulty level ("beginner", "intermediate", "advanced")
        specific_topic: Optional specific topic within the category
        api_key: Optional OpenAI API key (if not set in environment)
    
    Returns:
        List of question dictionaries in the required format
    """

    # Construct the prompt
    prompt = f"""Generate {num_questions} {difficulty} level multiple choice questions about {category}."""
    
    prompt += f" Description of the category: {description}\n\n"
    
    prompt += """ Each question should be in the following JSON format:
{
    "category": "string",
    "question": "string",
    "options": {
        "A": "string",
        "B": "string",
        "C": "string",
        "D": "string"
    },
    "answer": "string (A, B, C, or D)"
}

DO NOT include any markdown code block markers in the response.
Requirements:
1. Questions should be realistic and practical
2. Options should be plausible but only one correct answer
3. Include scenario-based questions where appropriate
4. Make questions challenging but fair
5. Ensure answers are accurate and well-reasoned
6. Return only the JSON array, no additional text

Return the questions as a JSON array."""

    # Call GPT-4o
    # print(prompt)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000
    )

    # Extract and parse the JSON response
    try:
        questions = json.loads(response.choices[0].message.content)
        return questions
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print("Raw response:", response.choices[0].message.content)
        return []

def save_questions(
    questions: List[Dict],
    output_file: str,
) -> None:
    """
    Save generated questions to a JSON file. If the file exists, append the questions.
    If the file doesn't exist, create it with the questions as the first entries.
    
    Args:
        questions: List of question dictionaries
        output_file: Path to output JSON file
    """
    try:
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                existing_questions = json.load(f)
            all_questions = existing_questions + questions
        else:
            all_questions = questions

        with open(output_file, 'w') as f:
            json.dump(all_questions, f, indent=2)
            
        print(f"Successfully saved {len(questions)} questions to {output_file}")
    except Exception as e:
        print(f"Error saving questions: {e}")

def main():
    # Combine both category dictionaries
    all_categories = {**general_categories, **security_tools_categories}
    
    # Initialize list to store all questions
    all_questions = []
    
    # Generate questions for each category
    for category, description in all_categories.items():
        print(f"\n{'='*80}")
        print(f"Generating questions for category: {category}")
        print(f"Description: {description}")
        print(f"{'='*80}\n")
        
        questions = generate_questions(
            category=category,
            num_questions=5,
            difficulty="advanced",
            description=description
        )
        
        # Print the generated questions
        print("\nGenerated Questions:")
        print(json.dumps(questions, indent=2))
        
        # Add to all questions
        all_questions.extend(questions)
        
        # Be polite to the API
        time.sleep(1)
    
    # Ask user if they want to save all questions
    output_file = "create-dataset/evaluation_data.json"
    save = input("\nDo you want to save all generated questions? (y/n): ").lower()
    if save == 'y':
        save_questions(all_questions, output_file=output_file)
        
        # Print summary
        print("\nDataset Summary:")
        for category in set(q['category'] for q in all_questions):
            category_count = sum(1 for q in all_questions if q['category'] == category)
            print(f"{category}: {category_count} questions")

if __name__ == "__main__":
    main()
    # q = [
    #         {
    #             "category": "Healthcare Cybersecurity",
    #             "question": "In a hospital setting, a vulnerability is discovered in a network-connected insulin pump that could allow an attacker to alter dosage settings. What is the most effective initial step for the hospital's cybersecurity team to mitigate this risk?",
    #             "options": {
    #                 "A": "Immediately disconnect all network-connected insulin pumps from the network until a patch is applied.",
    #                 "B": "Inform patients using the pumps about the vulnerability and advise them to monitor their glucose levels more frequently.",
    #                 "C": "Work with the device manufacturer to quickly develop and deploy a security patch addressing the vulnerability.",
    #                 "D": "Conduct a comprehensive risk assessment to evaluate the potential impact of the vulnerability on patient safety."
    #             },
    #             "answer": "C"
    #         }
    #     ]
    # save_questions(q)
    
    # with open('create-dataset/eval2.json', 'r') as f:
    #         existing_questions = json.load(f)
    # print(existing_questions)