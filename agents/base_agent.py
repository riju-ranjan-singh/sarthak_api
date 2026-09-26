from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ai_provider import GeminiProvider

class BaseAgent(ABC):
    def __init__(self):
        self.provider = GeminiProvider()
        
    @property
    @abstractmethod
    def intent_name(self) -> str:
        """Name of the intent this agent handles (e.g., 'travel')"""
        pass
        
    def process_media(self, audio_path: str, frames: List[str]) -> Dict[str, Any]:
        """
        Process the media using the AI provider tailored to this agent's intent.
        """
        print(f"[{self.__class__.__name__}] Processing media...")
        return self.provider.analyze_media(audio_path, frames, intent=self.intent_name)
    
    @abstractmethod
    def get_prompt_instructions(self) -> str:
        """
        Return the specific instructions/prompt for extracting the structured data for this agent.
        """
        pass
