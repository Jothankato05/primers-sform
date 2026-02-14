
import json
import os
from typing import Dict, Any, List

EXP_FILE = "experience_m3.json"

class ExperienceMonitor:
    """
    PHASE 5: EXPERIENCE (M3)
    Statistical feedback loop. Not narrative.
    """
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.stats: Dict[str, Dict[str, Any]] = {}
        if self.enabled:
            self._load()

    def _load(self):
        if os.path.exists(EXP_FILE):
            try:
                with open(EXP_FILE, 'r') as f:
                    self.stats = json.load(f)
            except:
                self.stats = {}

    def _save(self):
        if not self.enabled: return
        with open(EXP_FILE, 'w') as f:
            json.dump(self.stats, f, indent=2)

    def log_heuristic_result(self, heuristic_name: str, confidence: float, confirmed: bool = True):
        """
        Updates statistical priors for a heuristic.
        """
        if not self.enabled: return

        if heuristic_name not in self.stats:
            self.stats[heuristic_name] = {
                "uses": 0,
                "avg_confidence": 0.0,
                "success_rate": 1.0 # Optimistic start
            }

        entry = self.stats[heuristic_name]
        n = entry["uses"]
        
        # update running avg
        new_conf = ((entry["avg_confidence"] * n) + confidence) / (n + 1)
        
        entry["uses"] += 1
        entry["avg_confidence"] = new_conf
        
        # very basic success tracking, in real v5 confirmed comes from user feedback
        if not confirmed:
             # penalize success rate
             entry["success_rate"] = ((entry["success_rate"] * n) + 0.0) / (n + 1)
        
        self._save()

    def get_calibration(self, heuristic_name: str) -> float:
        """Returns complex calibration factor based on experience."""
        if heuristic_name not in self.stats:
             return 1.0
        
        entry = self.stats[heuristic_name]
        # If confidence is historically high but success rate is low, reduce trust
        return entry["success_rate"]
