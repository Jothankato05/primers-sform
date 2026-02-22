from typing import List, Dict, Any, Optional
from datetime import datetime
from cognition.models import PolicyViolation, PolicySeverity
from knowledge.store import KnowledgeStore

class AutonomousAuditor:
    """
    PHASE 9: AUTONOMOUS AUDITOR
    Proactively identifies architectural debt and prepares interventions.
    """
    def __init__(self, store: KnowledgeStore):
        self.store = store

    def identify_primary_debt(self) -> Optional[Dict[str, Any]]:
        """
        Scans the knowledge base for the file with the highest debt (Complexity/LOC).
        """
        analyses = self.store.get_all_analyses()
        if not analyses:
            return None

        # Sort by debt factors
        debt_list = []
        for source, data in analyses.items():
            score = data.get("loc", 0) + (data.get("class_count", 0) * 50)
            debt_list.append({"source": source, "debt": score, "data": data})

        debt_list.sort(key=lambda x: x["debt"], reverse=True)
        return debt_list[0] if debt_list else None

    def prepare_proactive_alert(self, health_score: int) -> Optional[str]:
        """
        Generates a proactive warning if the system is drifting.
        """
        if health_score < 100: # Lowered for testing, usually < 80
            target = self.identify_primary_debt()
            if target:
                return f"PROACTIVE AUDIT: Structural integrity has dropped to {health_score}%. Primary debt detected in `{target['source']}`. Optimize codebase?"
        return None
