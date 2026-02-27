
import os
import json
from datetime import datetime
from typing import Dict, Any, List

class ExecutiveInsights:
    """
    COMMERCIAL LAYER: Transforms raw architectural data into high-level business intelligence.
    Designed for CTO/VPE personas to track ROI, Risk, and Velocity.
    """
    def __init__(self, m2_store):
        self.m2 = m2_store

    def generate_report(self) -> Dict[str, Any]:
        """
        Derives an executive summary from the M2 database.
        """
        # 1. Fetch Analyses
        analyses = self.m2.get_all_analyses()
        total_nodes = len(analyses)
        
        # 2. Calculate "Architectural Debt" Coefficient
        debt_score = self._calculate_debt(analyses)
        
        # 3. Estimated "Refactor Cost" (Market Value)
        # 1 debt point = $150 (approx. developer hour cost)
        estimated_cost = debt_score * 150
        
        # 4. Success Potential
        # Based on how well patterns are established
        roi_potential = self._calculate_roi(analyses)

        # 5. Ecosystem Breath
        projects = set()
        for source in analyses.keys():
            # Assume source paths like 'c:/.../scratch/project-name/file.py'
            if "scratch" in source:
                parts = source.split("scratch")[1].split(os.sep)
                if len(parts) > 1:
                    projects.add(parts[1])
        
        ecosystem_depth = len(projects) if projects else 1

        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "total_structural_units": total_nodes,
                "project_ecosystem_depth": ecosystem_depth,
                "architectural_health": max(0, 100 - (debt_score / 10)),
                "technical_debt_cost": estimated_cost,
                "velocity_risk": "HIGH" if debt_score > 500 else "STABLE",
                "roi_potential": f"{roi_potential}%"
            },
            "recommendations": self._generate_recommendations(debt_score, total_nodes),
            "market_verdict": self._get_market_verdict(debt_score)
        }

    def _calculate_debt(self, analyses: Dict) -> float:
        # Placeholder for complex heuristic: units * (average_complexity ^ 1.2)
        return len(analyses) * 4.5 # Example multiplier

    def _calculate_roi(self, analyses: Dict) -> int:
        # ROI is higher if the code is modular
        if not analyses: return 0
        return min(98, 50 + (len(analyses) // 2))

    def _generate_recommendations(self, debt: float, nodes: int) -> List[str]:
        recs = []
        if debt > 1000:
            recs.append("CRITICAL: Immediate refactor of god-objects required to prevent velocity collapse.")
        if nodes < 10:
            recs.append("GROWTH: Expand core logic to increase market depth.")
        else:
            recs.append("STABILITY: Maintain current modular pattern for high-velocity output.")
        return recs

    def _get_market_verdict(self, debt: float) -> str:
        if debt < 500:
            return "ENTERPRISE READY - High Scalability Potential"
        elif debt < 1500:
            return "TRANSITIONAL - Moderate Maintenance Overhead"
        else:
            return "DEBT HEAVY - Higher Operational Risk"
