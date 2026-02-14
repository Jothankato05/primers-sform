
# 🔹 PRIMERS REPOSITORY INTELLIGENCE
# --------------------------------
# Provides semantic search and analysis for local/remote codebases.

import re
from typing import List, Dict, Any

class KnowledgeGraph:
    def __init__(self):
        self.nodes: Dict[str, Any] = {}
        self.edges: List[Dict[str, str]] = []

    def add_node(self, name: str, node_type: str, metadata: Dict):
        self.nodes[name] = {"type": node_type, "meta": metadata}

    def add_edge(self, source: str, target: str, relation: str):
        self.edges.append({"source": source, "target": target, "relation": relation})

    def find_related(self, query: str) -> List[Dict]:
        results = []
        for name, data in self.nodes.items():
            if query.lower() in name.lower() or query.lower() in str(data["meta"]).lower():
                results.append({"name": name, "data": data})
        return results

class RepoAnalyst:
    def __init__(self):
        self.graph = KnowledgeGraph()
        self.trace_log: List[str] = []

    def log_step(self, msg: str):
        self.trace_log.append(msg)

    def analyze_chunk(self, content: str, source: str):
        """
        Extracts entities and adds to graph with heuristics.
        """
        lines = content.split('\n')
        imports = []
        functions = []
        classes = []
        
        for line in lines:
            line = line.strip()
            # Imports
            if line.startswith('import ') or line.startswith('from '):
                imports.append(line)
            # Classes
            elif line.startswith('class '):
                name = line.split('class ')[1].split('(')[0].split(':')[0]
                classes.append(name)
                self.graph.add_node(name, "class", {"source": source, "complexity": 1})
            # Functions
            elif line.startswith('def '):
                name = line.split('def ')[1].split('(')[0]
                functions.append(name)
                self.graph.add_node(name, "function", {"source": source, "complexity": 1})

        # Heuristic: file responsibility
        file_complexity = len(imports) + len(functions) + len(classes)
        role = "worker"
        if len(imports) > 5:
            role = "coordinator"
        elif len(classes) > 2:
            role = "god_object_candidate"
        
        self.graph.add_node(source, "file", {
            "role": role, 
            "imports": len(imports),
            "complexity": file_complexity
        })
        
        self.log_step(f"Analyzed {source}: Found {len(classes)} classes, {len(functions)} functions. Role: {role}")

    def get_insights(self, query: str) -> str:
        hits = self.graph.find_related(query)
        if not hits:
            return "No specific code entities found matching that query."
        
        summary = "Analysis Results:\n"
        for h in hits:
            meta = h['data']['meta']
            summary += f"- [{h['data']['type'].upper()}] {h['name']} ({meta.get('role', 'standard')})\n"
            if 'complexity' in meta:
                 summary += f"  (Complexity: {meta['complexity']}/10)\n"
        return summary

    def get_smells(self) -> List[str]:
        smells = []
        for name, node in self.graph.nodes.items():
            if node['type'] == 'file' and node['meta'].get('complexity', 0) > 10:
                smells.append(f"High Complexity Module: {name} (Score: {node['meta']['complexity']})")
            if node['type'] == 'file' and node['meta'].get('role') == 'god_object_candidate':
                smells.append(f"God Object Risk: {name} handles too many classes.")
        return smells if smells else ["Codebase appears clean based on current heuristics."]
