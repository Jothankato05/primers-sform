
from enum import Enum, auto

class Intent(Enum):
    EMPIRICAL_ANALYSIS = auto()
    COMPARATIVE_REASONING = auto()
    PLANNING = auto()
    EXPLANATION = auto()
    VALIDATION = auto()
    INGESTION = auto()
    KNOWLEDGE_ACQUISITION = auto()
    FALLBACK = auto()

class IntentRouter:
    def route(self, user_input: str) -> Intent:
        normalized = user_input.lower()
        
        if "compare" in normalized or "vs" in normalized:
            return Intent.COMPARATIVE_REASONING
        if "plan" in normalized and "refactor" in normalized:
            return Intent.PLANNING
        if "analyze" in normalized or "review" in normalized:
            return Intent.EMPIRICAL_ANALYSIS
        if "why" in normalized or "explain" in normalized:
            return Intent.EXPLANATION
        if "validate" in normalized or "check" in normalized:
            return Intent.VALIDATION
        if "ingest" in normalized:
            return Intent.INGESTION
        if "learn" in normalized or "github" in normalized:
            return Intent.KNOWLEDGE_ACQUISITION
        
        return Intent.FALLBACK
