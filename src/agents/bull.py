from src.agents.base import Agent
from src.core.llm import llm_client

class Bull(Agent):
    def __init__(self):
        super().__init__("The Glorifier", "Optimistic Analyst")

    def think(self, context: str) -> str:
        prompt = f"""
        You are The Glorifier (Bull Agent).
        Your goal is to find the UPSIDE, the MOAT, and the OPTIONALITY.
        Interpret the data optimistically. Focus on TAM, Growth, and Vision.
        
        Context:
        {context}
        
        Provide your argument.
        """
        return llm_client.generate(prompt)
