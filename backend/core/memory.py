
from typing import Dict, List, Any, Optional

class SessionContext:
    def __init__(self):
        self.active_repo: Optional[str] = None
        self.history: List[Dict[str, Any]] = []
        self.cached_graphs: Dict[str, Any] = {}
        self.confidence_trend: List[float] = []

    def update_confidence(self, score: float):
        self.confidence_trend.append(score)

    def log_command(self, step_data: Dict[str, Any]):
        self.history.append(step_data)

    def get_last_entry(self) -> Optional[Dict[str, Any]]:
        return self.history[-1] if self.history else None

