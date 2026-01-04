import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    EXA_API_KEY = os.getenv("EXA_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    FMP_API_KEY = os.getenv("FMP_API_KEY")
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-pro-latest")

config = Config()
