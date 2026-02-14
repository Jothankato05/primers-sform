
import sqlite3
import json
import hashlib
from typing import Dict, Optional, Any
from datetime import datetime

class KnowledgeStore:
    def __init__(self, db_path: str = "primers_knowledge.db", enabled: bool = True):
        self.enabled = enabled
        self.db_path = db_path
        if enabled:
            self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # M2 Schema: Strictly Factual
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS repo_analysis (
                    repo_hash TEXT PRIMARY KEY,
                    source_name TEXT,
                    files_count INTEGER,
                    avg_complexity REAL,
                    last_analyzed TEXT,
                    analysis_blob TEXT
                )
            """)
            conn.commit()

    def save_analysis(self, source: str, metrics: Dict[str, Any]):
        if not self.enabled: return

        # Create deterministic ID from source name (or file content hash in real world)
        repo_hash = hashlib.sha256(source.encode()).hexdigest()
        blob = json.dumps(metrics)
        timestamp = datetime.now().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO repo_analysis 
                (repo_hash, source_name, files_count, avg_complexity, last_analyzed, analysis_blob)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (repo_hash, source, metrics.get('files', 1), metrics.get('complexity', 0), timestamp, blob))
            conn.commit()

    def get_baseline(self, source_name: str) -> Optional[Dict[str, Any]]:
        if not self.enabled: return None

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT analysis_blob FROM repo_analysis WHERE source_name = ?", (source_name,))
            row = cursor.fetchone()
            return json.loads(row[0]) if row else None
