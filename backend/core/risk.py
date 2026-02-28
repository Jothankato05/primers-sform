
import os
import subprocess
import json
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

@dataclass
class RiskNode:
    source: str
    structural_risk: float = 0.0  # Complexity/LOC
    volatility_risk: float = 0.0  # Churn/Change freq
    author_risk: float = 0.0      # Knowledge silos
    blast_radius: float = 0.0     # Dependencies impacted
    total_risk_score: float = 0.0
    classification: str = "GREEN" # RED, ORANGE, YELLOW, BLUE

class RiskScoringCore:
    """
    V4 CORE: The mathematical engine for systemic fragility mapping.
    Integrates static analysis with git-based volatility.
    """
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.risk_data: Dict[str, RiskNode] = {}

    def compute_risk(self, analyses: Dict[str, Any], ecosystem_graph: Dict[str, List[str]]) -> Dict[str, RiskNode]:
        """
        Computes multi-dimensional risk for every node in the ecosystem.
        """
        # 1. Structural Risk (Static)
        for source, data in analyses.items():
            node = RiskNode(source=source)
            complexity = data.get("complexity", 1.0)
            loc = data.get("loc", 1.0)
            # Logarithmic scaling for structural risk
            node.structural_risk = (complexity * 0.7) + (loc / 100 * 0.3)
            self.risk_data[source] = node

        # 2. Volatility Risk (Git Churn)
        self._calculate_volatility_and_author_risk()

        # 3. Blast Radius (Network Centrality)
        self._calculate_blast_radius(ecosystem_graph)

        # 4. Total Score & Classification
        for node in self.risk_data.values():
            # Normalized weighted average
            node.total_risk_score = (
                (node.structural_risk * 0.4) + 
                (node.volatility_risk * 0.3) + 
                (node.blast_radius * 0.3)
            )
            
            # Layered Classification
            if node.total_risk_score > 80: node.classification = "RED"    # Structural Instability
            elif node.total_risk_score > 60: node.classification = "ORANGE" # Economic Risk
            elif node.total_risk_score > 40: node.classification = "YELLOW" # Governance
            elif node.blast_radius > 70: node.classification = "BLUE"      # High Criticality
            else: node.classification = "GREEN"

        return self.risk_data

    def _calculate_volatility_and_author_risk(self):
        """
        Analyzes git history to find hotspots and siloed dependencies.
        """
        try:
            # Get changes per file in the last 90 days
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

            # Normalize and apply to nodes
            max_churn = max(churn_map.values()) if churn_map else 1
            for path, churn in churn_map.items():
                # We need to fuzzy match file paths to our analysis keys
                for node_path in self.risk_data.keys():
                    if path in node_path:
                        self.risk_data[node_path].volatility_risk = (churn / max_churn) * 100
                        authors = len(author_map.get(path, []))
                        if authors == 1: self.risk_data[node_path].author_risk = 80.0
                        elif authors < 3: self.risk_data[node_path].author_risk = 40.0

        except Exception as e:
            print(f"Risk Core: Git analysis failed - {e}")

    def _calculate_blast_radius(self, graph: Dict[str, List[str]]):
        """
        Calculates how many nodes are impacted if this node fails (Transitive Fan-in).
        """
        in_degree = {}
        for source, deps in graph.items():
            for dep in deps:
                in_degree[dep] = in_degree.get(dep, 0) + 1
        
        max_in = max(in_degree.values()) if in_degree else 1
        for dep, count in in_degree.items():
            for node_path in self.risk_data.keys():
                if dep in node_path:
                    self.risk_data[node_path].blast_radius = (count / max_in) * 100
