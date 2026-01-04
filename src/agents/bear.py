from src.agents.base import Agent
from src.core.llm import llm_client

class Bear(Agent):
    def __init__(self):
        super().__init__("The Discriminator", "Skeptical Analyst")

    def think(self, context: str) -> str:
        prompt = f"""
        You are The Discriminator (Bear Agent).
        Your goal is to find the RISKS, the ACCOUNTING FLAWS, and the COMPETITION.
        Interpret the data skeptically. Focus on Margin Compression, Debt, and Execution Risk.
        
        Context:
        {context}
        
        Provide your argument.
        """
        return llm_client.generate(prompt)
