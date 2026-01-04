from src.core.llm import llm_client
from src.tools.search import search_tool
import re

class ThemeHunter:
    def __init__(self):
        pass

    def expand_query(self, user_query: str) -> list[str]:
        prompt = f"""
        You are an expert financial analyst.
        Convert the following vague user intent into 3 specific search queries that will help find relevant publicly traded companies.
        Focus on finding lists of companies, industry reports, or government policies affecting the sector.
        
        User Query: "{user_query}"
        
        Output ONLY a python list of strings. Example: ["Indian drone manufacturers listed", "PLI scheme for drone industry beneficiaries", "Defense companies with UAV contracts"]
        """
        response = llm_client.generate(prompt)
        # Basic parsing to ensure we get a list
        try:
            # simple cleanup to handle potential markdown code blocks
            clean_response = response.replace("```python", "").replace("```", "").strip()
            return eval(clean_response)
        except:
            return [user_query]

    def extract_tickers(self, search_results) -> list[str]:
        # In a real implementation, we would parse the content of the search results.
        # For now, we will use the LLM to infer tickers from the titles/snippets.
        
        context = "\n".join([f"Title: {r.title}\nURL: {r.url}" for r in search_results])
        
        prompt = f"""
        Identify the stock tickers of publicly traded companies mentioned or implied in the following search results.
        Focus on Indian companies (NSE/BSE) if the context implies India, otherwise global.
        Return ONLY a python list of ticker symbols (e.g., ['RELIANCE', 'TCS']).
        If no companies are found, return [].
        
        Search Results:
        {context}
        """
        response = llm_client.generate(prompt)
        try:
             clean_response = response.replace("```python", "").replace("```", "").strip()
             return eval(clean_response)
        except:
            return []

    def run(self, user_query: str) -> list[str]:
        print(f"Hunting for theme: {user_query}")
        
        # 1. Expand Query
        queries = self.expand_query(user_query)
        print(f"Expanded Queries: {queries}")
        
        all_results = []
        for q in queries:
            results = search_tool.search(q, num_results=3)
            all_results.extend(results)
            
        # 2. Extract Tickers
        tickers = self.extract_tickers(all_results)
        
        # Deduplicate
        tickers = list(set(tickers))
        print(f"Found Tickers: {tickers}")
        return tickers
