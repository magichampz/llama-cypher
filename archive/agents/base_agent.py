from abc import ABC, abstractmethod
from typing import Any, Dict
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage

class BaseAgent(ABC):
    def __init__(self, model_name: str = "llama3.1:8b"):
        self.llm = ChatOllama(model=model_name)
        self.system_prompt = self._get_system_prompt()
    
    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Return the system prompt for this specific agent."""
        pass
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the input data and return the results."""
        pass
    
    def _call_llm(self, user_message: str) -> str:
        """Make a call to the LLM with the given user message."""
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_message)
        ]
        response = self.llm.invoke(messages)
        return response.content 