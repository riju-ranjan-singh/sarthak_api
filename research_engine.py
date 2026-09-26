from duckduckgo_search import DDGS
from typing import Dict, Any, List

class WebResearchModule:
    def __init__(self):
        self.ddgs = DDGS()
        
    def search(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """
        Searches the web for current information.
        """
        print(f"[WebResearchModule] Searching web for: {query}")
        try:
            results = list(self.ddgs.text(query, max_results=max_results))
            return [{"title": r["title"], "snippet": r["body"], "url": r["href"]} for r in results]
        except Exception as e:
            print(f"[WebResearchModule] Search failed: {e}")
            return []

class VerificationEngine:
    def __init__(self):
        self.research_module = WebResearchModule()
        
    def verify_analysis(self, intent: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes the raw JSON output from the AI and performs web research on key items.
        Appends VERIFIED information.
        """
        print(f"[VerificationEngine] Verifying data for intent: {intent}")
        verified_info = []
        
        # Simple MVP logic: if it's a shopping video, verify product prices.
        if intent == "shopping" and analysis_data.get("products"):
            for product in analysis_data["products"]:
                search_results = self.research_module.search(f"{product} current price online")
                if search_results:
                    verified_info.append(
                        f"VERIFIED: Found {product} online. Snippet: {search_results[0]['snippet']} (Source: {search_results[0]['url']})"
                    )
                    
        elif intent == "travel" and analysis_data.get("hotels"):
             for hotel in analysis_data["hotels"]:
                search_results = self.research_module.search(f"{hotel} reviews price")
                if search_results:
                    verified_info.append(
                        f"VERIFIED: {hotel} - {search_results[0]['snippet']} (Source: {search_results[0]['url']})"
                    )
        
        # For anything else, we just pass it through
        analysis_data["verified_information"] = verified_info
        return analysis_data
