# from langchain_community.llms import ChatOllama
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
# from tools import scan_network, web_search, cve_search
from src.tools import scan_network, web_search, cve_search

# Initialize the LLM
# llm = ChatOllama(model="llama3.2:1b")
llm = ChatOllama(model="llama3b-instruct-og")


# The tools are already decorated with @tool, so we can use them directly
tools = [scan_network, web_search, cve_search]

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a cybersecurity assistant that helps analyze network security.
    You have access to tools that can scan networks, search for vulnerabilities, and look up CVE information.
    Only use the tools if you do not have information about the subject being asked.
    If you don't have enough information to use a tool, ask for clarification."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create memory for conversation history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create the agent
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

def main():
    # Example prompts to test the agent
    test_prompts = [
        # "check devices on my network",
        # "tell me about the vulnerabilities associated with the commvault command centre",
        # "tell me about CVE-2023-1234",
        # "tell me about the CVE with ID CVE-2025-34028",
        "do you know anything about the CVE-2021-44228 vulnerability",
        # "tell me about any CVEs you found",
    ]
    
    for prompt in test_prompts:
        print(f"\nTesting prompt: {prompt}")
        try:
            response = agent_executor.invoke({"input": prompt})
            print(f"Response: {response['output']}")
        except Exception as e:
            print(f"Error processing prompt: {str(e)}")

if __name__ == "__main__":
    main() 