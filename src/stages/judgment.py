from src.agents.bull import Bull
from src.agents.bear import Bear
from src.agents.judge import Judge
from src.agents.librarian import Librarian
from src.tools.finance import finance_tool

class Tribunal:
    def __init__(self):
        self.bull = Bull()
        self.bear = Bear()
        self.judge = Judge()
        self.librarian = Librarian()

    def run(self, ticker: str) -> dict:
        print(f"Starting Tribunal for {ticker}")
        
        # Initial Context
        metrics = finance_tool.get_metrics(ticker)
        news = finance_tool.get_news(ticker)
        
        # Fetch full financials for deep context
        financials = finance_tool.get_financials(ticker)
        financial_summary = "Full Financials (Income Stmt, Balance Sheet, Cash Flow) are available for analysis."
        if financials:
            # Add a brief summary of available years
            years = financials['income_stmt'].index.tolist() if financials['income_stmt'] is not None else []
            financial_summary += f" Data available for years: {years}"
        
        initial_context = f"Ticker: {ticker}\nMetrics: {metrics}\nNews: {news}\n{financial_summary}"
        
        history = [f"Initial Data: {initial_context}"]
        
        max_loops = 5 # Reduced for prototype speed
        loop = 0
        
        while loop < max_loops:
            print(f"--- Loop {loop + 1} ---")
            
            # 1. Agents Debate
            bull_arg = self.bull.think(history[-1])
            bear_arg = self.bear.think(history[-1])
            
            history.append(f"Bull: {bull_arg}")
            history.append(f"Bear: {bear_arg}")
            
            print(f"Bull: {bull_arg[:100]}...")
            print(f"Bear: {bear_arg[:100]}...")
            
            # 2. Judge Evaluates
            evaluation = self.judge.evaluate(history)
            score = evaluation.get("score", 0)
            print(f"Judge Score: {score}")
            
            if score > 90:
                print("Consensus Reached!")
                return {
                    "ticker": ticker,
                    "verdict": evaluation.get("verdict"),
                    "score": score,
                    "history": history
                }
            
            # 3. Directive Execution
            directive = evaluation.get("directive")
            if directive:
                print(f"Judge Directive: {directive}")
                # Pass ticker to librarian for context-aware execution (e.g. fetching financials)
                lib_result = self.librarian.execute_directive(directive, ticker=ticker)
                history.append(f"Librarian Result for '{directive}': {lib_result}")
            
            loop += 1
            
        print("Max loops reached. Returning uncertain verdict.")
        return {
            "ticker": ticker,
            "verdict": "Uncertain / Watchlist",
            "score": score,
            "history": history
        }
