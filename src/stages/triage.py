from src.tools.finance import finance_tool
from src.core.llm import llm_client

class Prism:
    def __init__(self):
        pass

    def analyze_narrative(self, ticker: str, metrics: dict, news: list[str]) -> str:
        """
        Decides whether to KEEP or DISCARD a stock based on metrics and narrative.
        """
        
        prompt = f"""
        You are "The Prism", a financial triage agent.
        Your goal is to rescue "ugly" stocks (bad metrics) if the narrative justifies it (e.g., massive expansion).
        
        Ticker: {ticker}
        Metrics:
        - P/E: {metrics.get('pe')}
        - Free Cash Flow: {metrics.get('fcf')}
        - Debt/Equity: {metrics.get('debt_to_equity')}
        
        Recent News Headlines:
        {news}
        
        Rules:
        1. IF Metrics are Good (e.g., P/E < 30, Positive FCF) -> PASSED.
        2. IF Metrics are Bad (e.g., P/E > 50 or Negative FCF) AND News implies "Expansion/CAPEX/Spin-off/New Product" -> PASSED (Gold Flag).
        3. IF Metrics are Bad AND News implies "Litigation/Fraud/Market Share Loss" -> DISCARD.
        4. If unsure, default to DISCARD.
        
        Output ONLY one word: PASSED or DISCARD.
        """
        
        response = llm_client.generate(prompt)
        return response.strip().upper()

    def run(self, tickers: list[str]) -> list[str]:
        print(f"Triaging tickers: {tickers}")
        passed_tickers = []
        
        for t in tickers:
            metrics = finance_tool.get_metrics(t)
            if not metrics:
                continue
                
            news = finance_tool.get_news(t)
            
            verdict = self.analyze_narrative(t, metrics, news)
            print(f"Ticker: {t}, Verdict: {verdict}")
            
            if "PASSED" in verdict:
                passed_tickers.append(t)
                
        return passed_tickers
