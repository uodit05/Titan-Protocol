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
            response = self.model.generate_content(prompt)
            return response.text
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented")

llm_client = LLM()
