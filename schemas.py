from typing import Optional, List
from pydantic import BaseModel, Field

class BaseAnalysis(BaseModel):
    content_type: str
    title: str = Field(description="A short, catchy title for the content.")
    summary: str = Field(description="A brief summary of what the video or image is about.")
    inferences: List[str] = Field(default_factory=list, description="Things inferred by AI.")
    spoken_claims: List[str] = Field(default_factory=list, description="Important claims spoken explicitly.")
    on_screen_text: List[str] = Field(default_factory=list, description="Important text detected on screen.")
    timestamps: List[str] = Field(default_factory=list, description="List of important timestamps in MM:SS - Description format.")
    verified_information: List[str] = Field(default_factory=list, description="Information independently checked through external web research.")

class TravelPlanRequest(BaseModel):
    origin: str
    destination: str
    date: str
    duration: str
    travelers: str
    budget: str

class GeneralAnalysis(BaseAnalysis):
    pass

class TravelAnalysis(BaseAnalysis):
    locations: List[str] = Field(default_factory=list, description="Places, cities, or landmarks mentioned.")
    hotels: List[str] = Field(default_factory=list, description="Hotels or stays mentioned.")
    activities: List[str] = Field(default_factory=list, description="Activities to do.")
    prices: List[str] = Field(default_factory=list, description="Prices of travel items or total budget.")

class ShoppingAnalysis(BaseAnalysis):
    products: List[str] = Field(default_factory=list, description="Products shown or mentioned.")
    brands: List[str] = Field(default_factory=list, description="Brands mentioned.")
    prices: List[str] = Field(default_factory=list, description="Prices of the products.")
    features: List[str] = Field(default_factory=list, description="Product features and specs.")

class RecipeAnalysis(BaseAnalysis):
    ingredients: List[str] = Field(default_factory=list, description="List of ingredients with quantities.")
    steps: List[str] = Field(default_factory=list, description="Cooking steps.")
    cooking_time: Optional[str] = Field(default=None, description="Total cooking or prep time.")

class FoodAnalysis(BaseAnalysis):
    restaurants: List[str] = Field(default_factory=list, description="Restaurants mentioned.")
    dishes: List[str] = Field(default_factory=list, description="Specific dishes or cuisines shown.")
    prices: List[str] = Field(default_factory=list, description="Cost of the food.")

class FitnessAnalysis(BaseAnalysis):
    exercises: List[str] = Field(default_factory=list, description="Exercises mentioned.")
    reps_and_sets: List[str] = Field(default_factory=list, description="Reps and sets for exercises.")
    form_cues: List[str] = Field(default_factory=list, description="Tips on form and execution.")

class TechTutorialAnalysis(BaseAnalysis):
    software_hardware: List[str] = Field(default_factory=list, description="Software or hardware mentioned.")
    steps: List[str] = Field(default_factory=list, description="Step-by-step instructions.")
    code_snippets: List[str] = Field(default_factory=list, description="Code or commands shown.")

class FashionAnalysis(BaseAnalysis):
    clothing_items: List[str] = Field(default_factory=list, description="Specific clothing items or accessories.")
    brands: List[str] = Field(default_factory=list, description="Fashion brands mentioned.")
    aesthetics: List[str] = Field(default_factory=list, description="Style or aesthetic names.")

class DIYAnalysis(BaseAnalysis):
    tools_needed: List[str] = Field(default_factory=list, description="Tools required for the project.")
    materials: List[str] = Field(default_factory=list, description="Materials and supplies needed.")
    steps: List[str] = Field(default_factory=list, description="Step-by-step instructions.")
    total_cost: Optional[str] = Field(default=None, description="Total estimated cost.")

class FinanceAnalysis(BaseAnalysis):
    topics: List[str] = Field(default_factory=list, description="Financial topics discussed.")
    frameworks: List[str] = Field(default_factory=list, description="Rules or frameworks (e.g., 50/30/20).")
    tickers: List[str] = Field(default_factory=list, description="Stock tickers or assets mentioned.")

class MediaRecommendationAnalysis(BaseAnalysis):
    titles: List[str] = Field(default_factory=list, description="Books, movies, or shows mentioned.")
    creators: List[str] = Field(default_factory=list, description="Authors or directors.")
    genres: List[str] = Field(default_factory=list, description="Genres of the recommendations.")
    ratings: List[str] = Field(default_factory=list, description="Creator's ratings.")
