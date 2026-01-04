from src.agents.base import Agent
from src.tools.finance import finance_tool
from src.tools.search import search_tool
import pandas as pd

class Librarian(Agent):
    def __init__(self):
        super().__init__("Librarian", "Tool User")

    def execute_directive(self, directive: str) -> str:
        """
        Executes a specific directive from the Judge.
        Can use Python for calculations or Search/Finance tools.
        """
        # For simplicity, we'll use a basic routing logic or LLM to decide tool.
        # In a full implementation, this would be a ReAct loop.
        
        if "calculate" in directive.lower():
            # Safe python execution is hard. We'll simulate it for now or use a very restricted eval.
            # For the prototype, we will trust the LLM to generate valid python code to run on a dataframe if provided,
            # or just return a mocked calculation for the specific Grasim example if it matches.
            pass
            
        if "check" in directive.lower() or "search" in directive.lower():
            results = search_tool.search(directive, num_results=3)
            return f"Search Results for '{directive}':\n" + "\n".join([f"- {r.title}: {r.text[:200]}..." for r in results])
            
        return f"Librarian received directive: {directive}. (Tool execution placeholder)"

    def think(self, context: str) -> str:
        return "I await directives."
