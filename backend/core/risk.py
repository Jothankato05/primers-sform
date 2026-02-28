
import os
import subprocess
import json
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

@dataclass
class RiskNode:
    source: str
    structural_risk: float = 0.0  # S: Complexity/LOC
    volatility_risk: float = 0.0  # V: Churn/Change freq
    knowledge_risk: float = 0.0    # K: Author concentration (Bus Factor)
    criticality_risk: float = 0.0  # C: Centrality (Blast Radius)
    total_risk_score: float = 0.0
    classification: str = "GREEN"

class RiskScoringCore:
    """
    V4 CORE: The mathematical engine for systemic fragility mapping.
    Uses normalized sub-scores: RiskIndex = 100 * (wS*S + wV*V + wK*K + wC*C)
    """
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.risk_data: Dict[str, RiskNode] = {}
        # V4 Weights
        self.wS, self.wV, self.wK, self.wC = 0.30, 0.30, 0.15, 0.25

    def compute_risk(self, analyses: Dict[str, Any], ecosystem_graph: Dict[str, List[str]]) -> Dict[str, RiskNode]:
        """
        Computes multi-dimensional risk for every node in the ecosystem.
        """
        # 1. S: Structural Risk
        for source, data in analyses.items():
            node = RiskNode(source=source)
            complexity = data.get("complexity", 1.0)
            loc = data.get("loc", 1.0)
            # Logarithmic normalization for S
            node.structural_risk = min(1.0, (complexity / 20.0) * 0.7 + (loc / 500.0) * 0.3)
            self.risk_data[source] = node

        # 2. V & K: Volatility and Knowledge Risk
        self._calculate_git_metrics()

        # 3. C: Criticality Risk (Blast Radius)
        self._calculate_criticality(ecosystem_graph)

        # 4. Total Score & Classification
        for node in self.risk_data.values():
            node.total_risk_score = 100 * (
                (node.structural_risk * self.wS) + 
                (node.volatility_risk * self.wV) + 
                (node.knowledge_risk * self.wK) + 
                (node.criticality_risk * self.wC)
            )
            
            # V4 Classification Tiers
            if node.total_risk_score > 75: node.classification = "RED"    # Structural Instability
            elif node.total_risk_score > 50: node.classification = "ORANGE" # Economic Risk
            elif node.total_risk_score > 25: node.classification = "YELLOW" # Governance
            elif node.criticality_risk > 0.6: node.classification = "BLUE"  # High Criticality (Strategic Hub)
            else: node.classification = "GREEN"

        return self.risk_data

    def _calculate_git_metrics(self):
        """Analyzes git history for churn (V) and author silos (K)."""
        try:
            cmd = ["git", "log", "--since=3.months.ago", "--name-only", "--pretty=format:%ae"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=self.workspace_root, text=True)
            stdout, _ = process.communicate()

            churn_map = {}
            author_map = {}
            current_author = None
            
            for line in stdout.split("\n"):
                line = line.strip()
                if not line: continue
                if "@" in line:
                    current_author = line
                elif os.path.exists(os.path.join(self.workspace_root, line)):
                    file_path = line
                    churn_map[file_path] = churn_map.get(file_path, 0) + 1
                    if file_path not in author_map: author_map[file_path] = set()
                    author_map[file_path].add(current_author)

            max_churn = max(churn_map.values()) if churn_map else 1
            for path, churn in churn_map.items():
                for node_path in self.risk_data.keys():
                    if path in node_path:
                        # V Score
                        self.risk_data[node_path].volatility_risk = min(1.0, churn / max_churn)
                        # K Score (Inverse of bus factor)
                        authors = len(author_map.get(path, []))
                        if authors == 1: self.risk_data[node_path].knowledge_risk = 0.9
                        elif authors == 2: self.risk_data[node_path].knowledge_risk = 0.5
                        else: self.risk_data[node_path].knowledge_risk = 0.1
        except Exception: pass

    def _calculate_criticality(self, graph: Dict[str, List[str]]):
        """Calculates Centrality (C) as representative of Blast Radius."""
        in_degree = {}
        for source, deps in graph.items():
            for dep in deps:
                in_degree[dep] = in_degree.get(dep, 0) + 1
        
        max_in = max(in_degree.values()) if in_degree else 1
        for dep, count in in_degree.items():
            for node_path in self.risk_data.keys():
                if dep in node_path:
                    self.risk_data[node_path].criticality_risk = min(1.0, count / max_in)
