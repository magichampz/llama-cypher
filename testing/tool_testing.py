# %% [markdown]
# # Testing LLM Tool Usage with LangChain and Ollama
# 
# This notebook demonstrates how to use LangChain tools with the Llama model through Ollama.

# %%
# Import required libraries
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, SystemMessage
import json

# %% [markdown]
# ## Define Test Tools
# 
# We'll create three tools for testing:
# 1. Network scanning
# 2. CVE checking
# 3. Report generation

# %%
@tool
def search_network(ip_range: str) -> str:
    """Search the network for devices in the given IP range."""
    # Simulate network search
    return f"Found devices in {ip_range}: Device1 (192.168.1.100), Device2 (192.168.1.101)"

@tool
def check_cve(device_type: str) -> str:
    """Check for known CVEs for a specific device type."""
    # Simulate CVE database check
    return f"Found CVEs for {device_type}: CVE-2023-1234 (Critical), CVE-2023-1235 (High)"

@tool
def generate_report(findings: str) -> str:
    """Generate a security report based on the findings."""
    # Simulate report generation
    return f"Security Report:\n{findings}\n\nRecommendations:\n1. Update firmware\n2. Implement network segmentation"

# %% [markdown]
# ## Set up the LLM and Agent

# %%
# Initialize the LLM
llm = ChatOllama(model="llama3.1:8b")

# Create a list of tools
tools = [search_network, check_cve, generate_report]

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a security assessment agent. Use the available tools to analyze the network and generate reports."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create the agent
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# %% [markdown]
# ## Test Cases
# 
# Let's run through three test cases to evaluate the agent's ability to use tools:
# 1. Simple network scan
# 2. CVE check for a specific device
# 3. Complex multi-step task

# %%
# Test 1: Simple network scan
print("Test 1: Simple network scan")
result1 = agent_executor.invoke({"input": "Scan the network 192.168.1.0/24 for devices"})
print("\nResult:")
print(json.dumps(result1, indent=2))

# %%
# Test 2: CVE check for specific device
print("Test 2: CVE check for specific device")
result2 = agent_executor.invoke({"input": "Check for vulnerabilities in the MRI scanner found at 192.168.1.100"})
print("\nResult:")
print(json.dumps(result2, indent=2))

# %%
# Test 3: Complex multi-step task
print("Test 3: Complex multi-step task")
result3 = agent_executor.invoke({"input": "Scan the network, check for vulnerabilities in any medical devices found, and generate a security report"})
print("\nResult:")
print(json.dumps(result3, indent=2))

# %% [markdown]
# ## Analysis
# 
# After running the tests above, we can analyze:
# 1. Did the agent choose the right tools for each task?
# 2. Did it chain tools together effectively?
# 3. Did it handle the tool outputs correctly?
# 4. Were there any unexpected behaviors? 