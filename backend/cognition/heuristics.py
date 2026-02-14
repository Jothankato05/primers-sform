
from typing import Dict, List
from cognition.models import AnalysisResult, Interpretation

class HeuristicEngine:
    """
    LAYER 2: INTERPRETATION
    Applies rules and baselines to the raw data.
    """
    def interpret(self, data: AnalysisResult, baseline: Dict[str, float]) -> Interpretation:
        # 1. Calculate Raw Complexity
        raw_complexity = len(data.classes) + len(data.functions) + len(data.imports)
        
        # 2. Compare to Baseline
        avg = baseline.get("avg_complexity", 10)
        if avg == 0: avg = 10
        relative_complexity = raw_complexity / avg

        # 3. Assign Role
        role = "worker"
        if len(data.imports) > (baseline.get("avg_imports", 5) * 1.5):
            role = "coordinator"
        if relative_complexity > 2.0:
            role = "god_object_candidate"
        if data.loc < 10:
            role = "stub"

        # 4. Detect Smells
        smells = []
        if relative_complexity > 2.5:
            smells.append(f"Excessive Complexity ({relative_complexity:.1f}x avg)")
        if len(data.classes) > 1 and len(data.functions) > 10:
            smells.append("Mixed Responsibilities (Classes + many functions)")

        return Interpretation(
            source=data.source,
            complexity_score=float(raw_complexity),
            role=role,
            smells=smells,
            relative_complexity=relative_complexity
        )
