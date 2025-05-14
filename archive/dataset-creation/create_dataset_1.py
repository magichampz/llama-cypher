import json
import time
from openai import OpenAI
import os

def generate_dataset():
    # Set up OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Categories to cover
    general_categories = {
        "Medical Device Vulnerabilities": "Explores weaknesses in medical devices that can be exploited by cyber threats.",
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
    
    # Generation types
    tasks = [
        "Explanatory Q&A",
        "Scenario-based Q&A",
    ]

    # How many examples per category-task combo
    examples_per_task_general = 4
    examples_per_task_security_tools = 2
    # Prompt templates
    PROMPT_TEMPLATES = {
        "Explanatory Q&A": (
            "Generate 2 cybersecurity training question and answer entries for the healthcare domain. "
            "Category: {category}. Category Description: {category_description}. Type: Explanatory Q&A. "
            "For each data entry, output a JSON object with ONLY 4 fields: 'category', 'task_type', 'question' and 'answer'. The question should ask for an explanation or overview, "
            "and the answer should give a detailed, clear explanation."
            " The answer should be concise but clear, ideally 2 to 3 sentences long."
            " Return the entries as a JSON array."
        ),
        "Scenario-based Q&A": (
            "Generate 2 scenario-based cybersecurity questions and answers for healthcare. "
            "Category: {category}. Category Description: {category_description}. Type: Scenario-based Q&A. "
            "For each data entry, output a JSON object with ONLY 4 fields: 'category', 'task_type', 'question' and 'answer'. The question should describe a realistic security problem scenario, "
            "and the answer should explain the best response or mitigation."
            " The answer should be concise but clear, ideally 2 to 3 sentences long."
            " Return the entries as a JSON array."
        ),
    }
    
    TOOL_PROMPT_TEMPLATE = (
        "Generate 2 cybersecurity training question and answer entries for the healthcare domain. "
        "Category: {category}. Category Description: {category_description}. Type: Tool-based question. "
        "For each data entry, output a JSON object with ONLY 4 fields: 'category', 'task_type', 'question', and 'answer'. "
        "The question should ask about the primary use or purpose of a specific Kali Linux tool. "
        "The answer should be concise but clear, ideally 1 to 2 sentences long. Return the entries as a JSON array."
    )   

    dataset = []

    for category in list(general_categories.keys()):
        for task in tasks:
            for i in range(examples_per_task_general):
                prompt = PROMPT_TEMPLATES[task].format(category=category, category_description=general_categories[category])
                prompt += "\n\nDO NOT include any markdown code block markers in the response."
                print("-"*50)
                try:
                    print(f"\nGenerating: {task} | {category} | Batch {i+1}")
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a cybersecurity expert specialized in healthcare security."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                    )
                    content = response.choices[0].message.content.strip()

                    # Strip markdown code block if present
                    if content.startswith("```"):
                        first_newline = content.find("\n")
                        last_backticks = content.rfind("```")
                        content_cleaned = content[first_newline + 1:last_backticks].strip()
                    else:
                        content_cleaned = content

                    # Try parsing JSON array
                    data_entries = json.loads(content_cleaned)
                    
                    # Ensure we have a list of entries
                    if not isinstance(data_entries, list):
                        data_entries = [data_entries]
                    
                    # Process each entry
                    for entry in data_entries:
                        # Add metadata if not present
                        if 'category' not in entry:
                            entry['category'] = category
                        if 'task_type' not in entry:
                            entry['task_type'] = task
                        
                        dataset.append(entry)
                        
                        # Print the generated example
                        print("\nGenerated Example:")
                        print(json.dumps(entry, indent=2))

                        # Write to file incrementally
                        with open("create-dataset/training_data.jsonl", "a") as f:
                            f.write(json.dumps(entry) + "\n")

                    # Be polite to the API
                    time.sleep(1)

                except Exception as e:
                    print(f"Error generating or parsing: {e}")
                    print(f"Raw response:\n{content}\n")
                    continue
                
                
    for category in list(security_tools_categories.keys()):
            for i in range(examples_per_task_security_tools):
                prompt = TOOL_PROMPT_TEMPLATE.format(category=category, category_description=security_tools_categories[category])
                prompt += "\n\nDO NOT include any markdown code block markers in the response."
                print("-"*50)
                try:
                    print(f"\nGenerating: {category} | Batch {i+1}")
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a cybersecurity expert specialized in healthcare security."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                    )
                    content = response.choices[0].message.content.strip()

                    # Strip markdown code block if present
                    if content.startswith("```"):
                        first_newline = content.find("\n")
                        last_backticks = content.rfind("```")
                        content_cleaned = content[first_newline + 1:last_backticks].strip()
                    else:
                        content_cleaned = content

                    # Try parsing JSON array
                    data_entries = json.loads(content_cleaned)
                    
                    # Ensure we have a list of entries
                    if not isinstance(data_entries, list):
                        data_entries = [data_entries]
                    
                    # Process each entry
                    for entry in data_entries:
                        # Add metadata if not present
                        if 'category' not in entry:
                            entry['category'] = category

                        
                        dataset.append(entry)
                        
                        # Print the generated example
                        print("\nGenerated Example:")
                        print(json.dumps(entry, indent=2))

                        # Write to file incrementally
                        with open("create-dataset/training_data.jsonl", "a") as f:
                            f.write(json.dumps(entry) + "\n")

                    # Be polite to the API
                    time.sleep(1)

                except Exception as e:
                    print(f"Error generating or parsing: {e}")
                    print(f"Raw response:\n{content}\n")
                    continue

    print(f"\nGenerated {len(dataset)} examples in total.")
    return dataset

def main():
    # Clear the output file if it exists
    with open("create-dataset/training_data.jsonl", "w") as f:
        pass
    
    # Generate the dataset
    dataset = generate_dataset()
    
    # Print summary
    print("\nDataset Summary:")
    for category in set(d['category'] for d in dataset):
        category_count = sum(1 for d in dataset if d['category'] == category)
        print(f"{category}: {category_count} examples")
    
    for task in set(d['task_type'] for d in dataset):
        task_count = sum(1 for d in dataset if d['task_type'] == task)
        print(f"{task}: {task_count} examples")

if __name__ == "__main__":
    main()
    # categories = {
    #     "Medical Device Vulnerabilities": "Explores weaknesses in medical devices that can be exploited by cyber threats.",
    #     "Bluetooth and Wireless Security": "Covers security measures and vulnerabilities related to Bluetooth and wireless technologies.",
    #     "Penetration Testing Workflows": "Describes the processes and methodologies used in penetration testing.",
    #     "Penetration Testing Lifecycle": "Details the stages involved in the lifecycle of penetration testing.",
    #     "Physical Attack Vectors": "Focuses on physical methods used to compromise security systems.",
    #     "Network and Application Exploits": "Examines vulnerabilities in networks and applications that can be exploited.",
    #     "Mitigation and Hardening": "Discusses strategies to strengthen systems against attacks and reduce vulnerabilities. Best practices for device-level, network-level, and application-level security",
    #     "Incident Response": "Covers the procedures and actions taken in response to security incidents.",
    #     "Compliance and Legal (HIPAA, MHRA, GDPR)": "Addresses legal and compliance requirements in cybersecurity, as well as Privacy and Data Protection.",
    # }
    
    # print(list(categories.keys())[0:2])
    # for category in categories.keys():
    #     print(category)
    #     print(categories[category])
    #     print("-"*50)