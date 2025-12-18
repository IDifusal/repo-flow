import os
import random
from typing import Protocol
from app.models.recipe import Recipe


class AIClient(Protocol):
    def recommend(self, recipes: list[Recipe]) -> int | None:
        ...


class MockAIClient:
    def recommend(self, recipes: list[Recipe]) -> int | None:
        if not recipes:
            return None
        return random.choice(recipes).id


def get_ai_client() -> AIClient:
    provider = os.getenv("AI_PROVIDER", "mock").lower()
    if provider == "mock":
        return MockAIClient()
    return MockAIClient()
