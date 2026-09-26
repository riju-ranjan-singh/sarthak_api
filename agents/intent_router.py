import os
from ai_provider import GeminiProvider
from agents.specialized_agents import (
    TravelAgent, ShoppingAgent, RecipeAgent, FoodAgent, GeneralAgent,
    FitnessAgent, TechTutorialAgent, FashionAgent, DIYAgent, FinanceAgent, MediaRecommendationAgent
)
from agents.base_agent import BaseAgent

class IntentRouter:
    def __init__(self):
        self.provider = GeminiProvider()
        self.agents = {
            "travel": TravelAgent(),
            "shopping": ShoppingAgent(),
            "recipe": RecipeAgent(),
            "food": FoodAgent(),
            "general": GeneralAgent(),
            "fitness": FitnessAgent(),
            "tech_tutorial": TechTutorialAgent(),
            "fashion": FashionAgent(),
            "diy": DIYAgent(),
            "finance": FinanceAgent(),
            "media_recommendation": MediaRecommendationAgent()
        }
        
    def determine_intent(self, audio_path: str, frames: list) -> BaseAgent:
        """
        Uses the GeminiProvider to quickly classify the content and returns the appropriate Agent.
        """
        print(f"[IntentRouter] Classifying content from {audio_path} and {len(frames)} frames...")
        
        # For MVP, we mock the intent detection.
        mock_intent = "travel"
        print(f"[IntentRouter] Detected intent: {mock_intent}")
        
        return self.agents.get(mock_intent, self.agents["general"])
