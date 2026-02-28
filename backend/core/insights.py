
import os
import json
from datetime import datetime
from typing import Dict, Any, List
from core.guardrails import SovereignGuardrails
from core.risk import RiskScoringCore

class ExecutiveInsights:
    """
    COMMERCIAL LAYER: Transforms raw architectural data into high-level business intelligence.
    Designed for CTO/VPE personas to track ROI, Risk, and Velocity.
    """
    def __init__(self, m2_store):
        self.m2 = m2_store
        self.guardrails = SovereignGuardrails()
        # Initialize Risk Engine with scratch root
        current_dir = os.path.dirname(__file__)
        scratch_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
        self.risk_engine = RiskScoringCore(scratch_root)

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
        
        # 6. Global Compliance
        violations = self.guardrails.audit_workspace(analyses)
        compliance_score = max(0, 100 - (len(violations) * 2))

        # 7. Systemic Fragility Mapping (V4 Core)
        graph = self.m2.get_graph()
        risk_nodes = self.risk_engine.compute_risk(analyses, graph)
        
        # Extract Top 3 Hotspots (Highest Total Risk)
        hotspots = sorted(risk_nodes.values(), key=lambda x: x.total_risk_score, reverse=True)[:3]
        fragility_report = [
            {
                "node": h.source,
                "score": round(h.total_risk_score, 1),
                "risk_type": h.classification,
                "blast_radius": round(h.blast_radius, 1)
            } for h in hotspots
        ]

        # 7. Predictive Savings Forecast
        # Total Units * Efficiency Multiplier * Avg Dev Day Cost
        annual_savings = (total_nodes * 250) + (compliance_score * 120)
        
        # 8. Repaid Debt (Sovereign Auto-Refactor)
        repaid_debt = self.m2.get_repaid_debt()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "total_structural_units": total_nodes,
                "project_ecosystem_depth": ecosystem_depth,
                "global_compliance_rating": f"{compliance_score}%",
                "architectural_health": max(0, 100 - (debt_score / 10)),
                "technical_debt_cost": estimated_cost,
                "total_debt_repaid": repaid_debt,
                "fragility_hotspots": fragility_report,
                "velocity_risk": "HIGH" if debt_score > 500 or any(h.total_risk_score > 70 for h in hotspots) else "STABLE",
                "roi_potential": f"{roi_potential}%",
                "annual_savings_forecast": annual_savings,
                "efficiency_roi": f"{(roi_potential * 1.4):.1f}%"
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
            recs.append("EXECUTION REQUIRED: Immediate liquidation of god-objects is mandatory to survive technical bankruptcy.")
        if nodes < 10:
            recs.append("EXPANSION MANDATE: Force-merge core logic into new modules to capture technical market share.")
        else:
            recs.append("DOMINANCE: Enforce the current modular pattern. Any deviation will be blocked by Sovereign Guardrails.")
        return recs

    def _get_market_verdict(self, debt: float) -> str:
        if debt < 500:
            return "ELITE STATUS - Pristine Architecture; Ready for Global Dominance"
        elif debt < 1500:
            return "WARNING - Structural Friction Detected; Executive Intervention Required"
        else:
            return "BANKRUPT - Technical Debt Overload; Halt All Development and Refactor"
