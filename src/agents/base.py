from src.core.llm import llm_client

class Agent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def think(self, context: str) -> str:
        raise NotImplementedError
