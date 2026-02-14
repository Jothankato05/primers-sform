
from typing import List, Dict
from cognition.models import AnalysisResult

class CodeAnalyzer:
    """
    LAYER 1: ANALYSIS
    Pure data extraction. No opinions.
    """
    def __init__(self):
        self.raw_data: Dict[str, AnalysisResult] = {}

    def analyze(self, content: str, source: str) -> AnalysisResult:
        lines = content.split('\n')
        result = AnalysisResult(source=source, loc=len(lines))
        
        for line in lines:
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                result.imports.append(line)
            elif line.startswith('class '):
                name = line.split('class ')[1].split('(')[0].split(':')[0]
                result.classes.append(name)
            elif line.startswith('def '):
                name = line.split('def ')[1].split('(')[0]
                result.functions.append(name)
        
        self.raw_data[source] = result
        return result

    def get_corpus_stats(self) -> Dict[str, float]:
        """Calculates baseline averages for the current corpus."""
        if not self.raw_data:
            return {"avg_complexity": 0, "avg_imports": 0}
        
        total_complexity = 0
        total_imports = 0
        count = len(self.raw_data)

        for res in self.raw_data.values():
            # Rough complexity metric for baseline calculation
            comp = len(res.classes) + len(res.functions) + len(res.imports)
            total_complexity += comp
            total_imports += len(res.imports)
        
        return {
            "avg_complexity": total_complexity / count,
            "avg_imports": total_imports / count
        }
