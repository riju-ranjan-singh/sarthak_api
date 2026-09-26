import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from agents.base_agent import BaseAgent

class TravelAgent(BaseAgent):
    @property
    def intent_name(self) -> str:
        return "travel"

    def get_prompt_instructions(self) -> str:
        return (
            "Analyze the travel content. Extract the locations, hotels, activities, and prices mentioned. "
            "Reconstruct the itinerary if possible. Provide a day-by-day plan."
        )

class ShoppingAgent(BaseAgent):
    @property
    def intent_name(self) -> str:
        return "shopping"

    def get_prompt_instructions(self) -> str:
        return (
            "Analyze the shopping/product content. Extract the products, brands, models, category, and price shown. "
            "List the features and the creator's claims."
        )

class RecipeAgent(BaseAgent):
    @property
    def intent_name(self) -> str:
        return "recipe"

    def get_prompt_instructions(self) -> str:
        return (
            "Analyze the recipe content. Extract ingredients with quantities, cooking steps, and cooking time. "
            "Convert the recipe into a grocery list format."
        )

class FoodAgent(BaseAgent):
    @property
    def intent_name(self) -> str:
        return "food"

    def get_prompt_instructions(self) -> str:
        return (
            "Analyze the food/restaurant content. Extract the restaurant name, location, dishes mentioned, cuisine, "
            "and prices."
        )

class GeneralAgent(BaseAgent):
    @property
    def intent_name(self) -> str:
        return "general"

    def get_prompt_instructions(self) -> str:
        return (
            "Analyze the content generally. Extract spoken claims, text on screen, and infer the main topic."
        )

class FitnessAgent(BaseAgent):
    @property
    def intent_name(self) -> str:
        return "fitness"

    def get_prompt_instructions(self) -> str:
        return "Analyze the workout content. Extract exercises, reps, sets, rest times, and form cues."

class TechTutorialAgent(BaseAgent):
    @property
    def intent_name(self) -> str:
        return "tech_tutorial"

    def get_prompt_instructions(self) -> str:
        return "Analyze the tech tutorial. Extract software/hardware mentioned, step-by-step instructions, and code snippets."

class FashionAgent(BaseAgent):
    @property
    def intent_name(self) -> str:
        return "fashion"

    def get_prompt_instructions(self) -> str:
        return "Analyze the fashion content. Extract clothing items, brands, and aesthetics mentioned."

class DIYAgent(BaseAgent):
    @property
    def intent_name(self) -> str:
        return "diy"

    def get_prompt_instructions(self) -> str:
        return "Analyze the DIY content. Extract tools needed, materials, steps, and total cost."

class FinanceAgent(BaseAgent):
    @property
    def intent_name(self) -> str:
        return "finance"

    def get_prompt_instructions(self) -> str:
        return "Analyze the finance content. Extract financial topics, budgeting frameworks, and stock tickers."

class MediaRecommendationAgent(BaseAgent):
    @property
    def intent_name(self) -> str:
        return "media_recommendation"

    def get_prompt_instructions(self) -> str:
        return "Analyze the book or movie review. Extract titles, creators, genres, and ratings."
