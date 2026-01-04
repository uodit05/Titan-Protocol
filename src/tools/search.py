from exa_py import Exa
from src.config import config

class SearchTool:
    def __init__(self):
        self.exa = Exa(api_key=config.EXA_API_KEY) if config.EXA_API_KEY else None

    def search(self, query: str, num_results: int = 5):
        if self.exa:
            response = self.exa.search(
                query,
                num_results=num_results,
                use_autoprompt=True
            )
            return response.results
        else:
            print("Warning: Exa API Key not found. Returning empty results.")
            return []

search_tool = SearchTool()
