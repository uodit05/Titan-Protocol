from src.agents.base import Agent
from src.core.llm import llm_client
import re

class Judge(Agent):
    def __init__(self):
        super().__init__("The Judge", "Evaluator")

    def evaluate(self, history: list[str]) -> dict:
        """
        Evaluates the current debate state.
        Returns a dict with:
        - satisfaction_score (0-100)
        - verdict (if score > 90)
        - directive (if score < 90)
        """
        history_text = "\n".join(history)
        
        prompt = f"""
        You are The Judge. You are overseeing a debate between a Bull and a Bear about a stock.
        
        Debate History:
        {history_text}
        
        Task:
        1. Assign a Satisfaction Score (0-100). Are all conflicts resolved? Do we have enough data?
        2. If Score > 90, provide a Final Verdict (Buy/Sell/Hold) and Reason.
        3. If Score < 90, identify the biggest Conflict or Data Gap and issue a specific Directive to the Librarian (e.g., "Check dealer onboarding numbers", "Calculate sum-of-parts").
        
        Output Format (JSON):
        {{
            "score": <int>,
            "verdict": "<string or null>",
            "directive": "<string or null>"
        }}
        """
        response = llm_client.generate(prompt)
        
        # Basic parsing
        try:
            # Clean up markdown
            clean = response.replace("```json", "").replace("```", "").strip()
            # In a real app, use json.loads. For now, we'll trust the LLM or use eval if simple.
            # Using eval for simplicity in prototype, but json.loads is safer.
            import json
            return json.loads(clean)
        except:
            print(f"Error parsing Judge response: {response}")
            return {"score": 0, "directive": "Analyze the financial statements."}

    def think(self, context: str) -> str:
        return "I am listening."
