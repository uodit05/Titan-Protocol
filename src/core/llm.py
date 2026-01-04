import google.generativeai as genai
from src.config import config
import os

class LLM:
    def __init__(self):
        self.provider = config.LLM_PROVIDER
        self.model_name = config.LLM_MODEL
        
        if self.provider == "gemini":
            genai.configure(api_key=config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(self.model_name)
        # Add other providers as needed

    def generate(self, prompt: str) -> str:
        if self.provider == "gemini":
            import time
            from google.api_core import exceptions
            
            max_retries = 5
            base_delay = 2
            
            for attempt in range(max_retries):
                try:
                    response = self.model.generate_content(prompt)
                    return response.text
                except exceptions.ResourceExhausted as e:
                    if attempt == max_retries - 1:
                        raise e
                    
                    delay = base_delay * (2 ** attempt)
                    print(f"Rate limit hit. Retrying in {delay} seconds...")
                    time.sleep(delay)
                except Exception as e:
                    raise e
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented")

llm_client = LLM()
