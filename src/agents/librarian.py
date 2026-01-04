from src.agents.base import Agent
from src.tools.finance import finance_tool
from src.tools.search import search_tool
import pandas as pd

class Librarian(Agent):
    def __init__(self):
        super().__init__("Librarian", "Tool User")

    def analyze_data(self, directive: str, dfs: dict) -> str:
        """
        Generates and executes pandas code to analyze financial data.
        """
        from src.core.llm import llm_client
        
        # Prepare context about available dataframes
        available_dfs = [k for k, v in dfs.items() if v is not None]
        if not available_dfs:
            return "No financial data available for analysis."
            
        prompt = f"""
        You are an expert Data Scientist.
        Your task is to write a Python pandas snippet to answer the following user directive.
        
        Directive: "{directive}"
        
        Available DataFrames (in local scope):
        - income_stmt (Rows: Years, Cols: Revenue, Net Income, etc.)
        - balance_sheet (Rows: Years, Cols: Assets, Liabilities, etc.)
        - cash_flow (Rows: Years, Cols: Operating Cash Flow, etc.)
        
        The DataFrames are already loaded. Years are in the index (most recent first usually, but check).
        
        Write ONLY the python code. The last line must be an expression that evaluates to the result (number or string), or print the result.
        Do NOT wrap in markdown blocks. Do NOT import pandas (it is already imported as pd).
        Example:
        income_stmt['Total Revenue'].pct_change().mean()
        """
        
        code = llm_client.generate(prompt).replace("```python", "").replace("```", "").strip()
        
        try:
            # Prepare local scope
            local_scope = {k: v for k, v in dfs.items() if v is not None}
            local_scope['pd'] = pd
            
            # Execute
            # We use exec to run the code, and capture the last expression if possible, 
            # but since exec doesn't return, we might need to wrap it or ask LLM to assign to a variable 'result'.
            # Let's adjust the prompt slightly or wrap the code.
            
            wrapped_code = f"""
try:
    result = {code}
except:
    # If it's not an expression, maybe it was a statement.
    {code}
    if 'result' not in locals():
        result = "Code executed but no 'result' variable found."
"""
            exec(wrapped_code, {}, local_scope)
            return str(local_scope.get('result', "No result returned."))
            
        except Exception as e:
            return f"Error executing analysis code: {e}\nCode was: {code}"

    def execute_directive(self, directive: str, ticker: str = None) -> str:
        """
        Executes a specific directive from the Judge.
        Can use Python for calculations or Search/Finance tools.
        """
        if "calculate" in directive.lower() or "analyze" in directive.lower():
            if ticker:
                # Fetch full financials
                dfs = finance_tool.get_financials(ticker)
                return self.analyze_data(directive, dfs)
            else:
                return "Librarian Error: Ticker required for calculation."
            
        if "check" in directive.lower() or "search" in directive.lower():
            results = search_tool.search(directive, num_results=3)
            return f"Search Results for '{directive}':\n" + "\n".join([f"- {r.title}: {r.text[:200]}..." for r in results])
            
        return f"Librarian received directive: {directive}. (Tool execution placeholder)"

    def think(self, context: str) -> str:
        return "I await directives."
