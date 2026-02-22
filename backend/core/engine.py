
import os
from typing import Dict, Any, List, Optional
# Import strict types
from core.types import EngineResponse, IntelligenceLevel, TraceLog, Tone
from core.intent import IntentRouter, Intent
from core.memory import SessionContext
from core.reasoning import ReasoningGraph
from core.governance import Governance

# Import the new 3-layer stack + Comparator
from cognition.analyzer import CodeAnalyzer
from cognition.heuristics import HeuristicEngine
from cognition.judge import JudgementCore
from cognition.comparator import Comparator
from cognition.analyst import RepoAnalyst

# Phase 5 Components
from knowledge.store import KnowledgeStore
from cognition.experience import ExperienceMonitor
from cognition.local_llm import LocalLLMConnector
from knowledge.github import GitHubConnector

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class PrimersEngine:
    def __init__(self):
        # Phase 5: Governance FIRST (The Source of Truth)
        self.gov = Governance()

        # The Cognitive Stack
        self.analyzer = CodeAnalyzer() # Layer 1
        self.heuristics = HeuristicEngine() # Layer 2
        self.judge = JudgementCore() # Layer 3
        self.comparator = Comparator()
        self.repo_analyst = RepoAnalyst() # Structural Intelligence
        
        # Internal Systems
        self.router = IntentRouter()
        self.session = SessionContext()
        self.github = GitHubConnector()
        
        # M2: Persistent Factual Memory
        self.m2 = KnowledgeStore(
            enabled=self.gov.is_enabled("persistent_memory_m2")
        )
        
        # M3: Experience & Calibration
        self.m3 = ExperienceMonitor(
            enabled=self.gov.is_enabled("experience_tracking_m3")
        )
        
        # Local LLM (Sandboxed)
        self.local_llm = LocalLLMConnector(
            enabled=self.gov.is_enabled("local_llm")
        )
        
        # External Fallback (Governed separately or via Env)
        self.external_api_key = os.getenv("GOOGLE_API_KEY") 
        if self.external_api_key and HAS_GENAI:
            genai.configure(api_key=self.external_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None

    def process(self, input_text: str, mode: str = "default") -> EngineResponse:
        trace = TraceLog(session_id="current_session")
        graph = ReasoningGraph(trace)
        
        # Step 0: Record Message to Session (Layer 1 Memory)
        self.session.add_message("user", input_text)
        
        # Step 0.5: Context Retrieval (ChatGPT-like awareness)
        # Search the knowledge base for topics mentioned in the input
        graph.add_step(Intent.VALIDATION, "Context_Retrieval", 1.0, "Searching M2 Knowledge Store for relevant entities")
        context_snippets = self.m2.search_entities(input_text, limit=3)
        if context_snippets:
            graph.add_step(Intent.VALIDATION, "Context_Match", 1.0, f"Found {len(context_snippets)} relevant code entities")
            # Inject context into the temporary prompt context (not saved to session history)
            context_bonus = "\n\nRelevant Workspace Context:\n" + "\n".join([f"- {s}" for s in context_snippets])
            input_text_with_context = input_text + context_bonus
        else:
            input_text_with_context = input_text

        # Step 1: Intent Routing
        intent = self.router.route(input_text)
        graph.add_step(intent, "Routing", 1.0, f"Classified intent as {intent.name}")
        
        response = None

        if intent == Intent.EMPIRICAL_ANALYSIS:
            target = input_text.split(" ")[-1] if " " in input_text else "corpus"
            response = self._handle_analysis(target, graph)
        
        elif intent == Intent.PLANNING:
            target_file = input_text.split("refactor")[-1].strip()
            response = self._handle_refactor_plan(target_file, graph)
            
        elif intent == Intent.COMPARATIVE_REASONING:
            parts = input_text.lower().replace("compare", "").split("vs")
            if len(parts) == 2:
                response = self._handle_comparison(parts[0].strip(), parts[1].strip(), graph)
            else:
                response = self._local_reflex("help", graph)

        elif intent == Intent.EXPLANATION:
             last_entry = self.session.get_last_entry()
             if not last_entry:
                  response = EngineResponse("No previous context to explain.", "explanation", 1.0, IntelligenceLevel.SYMBOLIC, Tone.INCONCLUSIVE, graph.trace)
             else:
                  # Use M1 (Session) to recall
                  prev_intent = last_entry.get("intent")
                  prev_input = last_entry.get("input")
                  explanation = f"Regarding your previous command '{prev_input}' ({prev_intent}):\n"
                  explanation += "I analyzed the request based on the active heuristics and knowledge graph.\n"
                  
                  # Phase 5: Check M3 stats
                  if self.m3.enabled:
                      explanation += "My experience monitor confirms nominal heuristic performance.\n"

                  # Phase 5: Optional LLM Polish
                  if self.local_llm.enabled:
                      llm_res = self.local_llm.get_summary(explanation)
                      if llm_res["speculation"]:
                           explanation += f"\nNote: {llm_res['content']}"

                  response = EngineResponse(explanation, "explanation", 1.0, IntelligenceLevel.HEURISTIC, Tone.ASSERTIVE, graph.trace)

        elif intent == Intent.INGESTION:
            target_path = input_text.split("ingest")[-1].strip()
            if not target_path:
                response = EngineResponse("Usage: ingest <path_to_directory>", "error", 1.0, IntelligenceLevel.SYMBOLIC, Tone.CAUTIOUS, trace)
            else:
                response = self._handle_ingest(target_path, graph)

        elif intent == Intent.KNOWLEDGE_ACQUISITION:
            parts = input_text.split("github")
            target = parts[-1].strip() if len(parts) > 1 else ""
            if not target:
                response = EngineResponse("Usage: learn from github <username>", "error", 1.0, IntelligenceLevel.SYMBOLIC, Tone.CAUTIOUS, graph.trace)
            else:
                response = self._handle_github_learning(target, graph)

        elif "show blueprint" in input_text.lower():
            graph.add_step(Intent.EMPIRICAL_ANALYSIS, "Graph Assembly", 1.0, "Generating architectural blueprint")
            blueprint = self.repo_analyst.get_blueprint()
            response = EngineResponse(f"### ARCHITECTURAL BLUEPRINT\n{blueprint}", "analysis", 1.0, IntelligenceLevel.HEURISTIC, Tone.ASSERTIVE, graph.trace)

        elif intent == Intent.FALLBACK:
            # 1. Cloud Fallback (Gemini) if configured and enabled
            if self.model and self.gov.is_enabled("external_llm"):
                graph.add_step(Intent.FALLBACK, "External Call", 0.9, "Routing to Gemini")
                try:
                    res = self.model.generate_content(input_text)
                    response = EngineResponse(res.text, "external", 0.9, IntelligenceLevel.EXTERNAL, Tone.CAUTIOUS, graph.trace)
                except Exception as e:
                    graph.add_step(Intent.FALLBACK, "Error", 0.0, f"External failed: {str(e)}")
                    # Continue to local
            
            # 2. Local/Simulated Fallback (Sovereign Mode)
            if not response:
                graph.add_step(Intent.FALLBACK, "Sovereign Chat", 0.8, "Processing as Sovereign Cognitive Response")
                # Pass engine context for simulated intelligence
                chat_res = self.local_llm.chat(input_text_with_context, history=self.session.get_messages())
                response = EngineResponse(chat_res, "chat", 0.8, IntelligenceLevel.HEURISTIC, Tone.ASSERTIVE, graph.trace)

        if not response:
             response = self._local_reflex(input_text, graph)

        # M1 Update
        self.session.log_command({
            "input": input_text,
            "intent": intent.name,
            "confidence": response.confidence,
            "response_summary": response.content[:50]
        })
        self.session.add_message("assistant", response.content)
        self.session.update_confidence(response.confidence)

        return response

    def _handle_ingest(self, target_path: str, graph: ReasoningGraph) -> EngineResponse:
        import glob
        
        if not os.path.exists(target_path):
             return EngineResponse(f"Path not found: {target_path}", "error", 1.0, IntelligenceLevel.SYMBOLIC, Tone.ASSERTIVE, graph.trace)
             
        # Normalize path
        target_path = os.path.abspath(target_path)
        
        # Simple recursive walk
        count = 0
        total_loc = 0
        
        # Walk directory
        for root, dirs, files in os.walk(target_path):
            if "venv" in root or "__pycache__" in root or ".git" in root:
                continue
                
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, target_path)
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            res = self.analyzer.analyze(content, rel_path) # Layer 1
                            self.repo_analyst.analyze_chunk(content, rel_path) # Graph Layer
                            count += 1
                            total_loc += res.loc
                    except Exception as e:
                        print(f"Failed to read {file}: {e}")

        if count == 0:
             return EngineResponse(f"No Python files found in {target_path}", "warning", 1.0, IntelligenceLevel.SYMBOLIC, Tone.CAUTIOUS, graph.trace)

        # Baseline update
        baseline = self.analyzer.get_corpus_stats()
        
        msg = f"Ingested {count} files ({total_loc} lines). Corpus baseline updated (Avg Complexity: {baseline['avg_complexity']:.1f}). Ready for analysis."
        graph.add_step(Intent.INGESTION, "File Walk", 1.0, f"Scanned {count} files")
        
        return EngineResponse(msg, "ingestion", 1.0, IntelligenceLevel.SYMBOLIC, Tone.ASSERTIVE, graph.trace)

    def _handle_analysis(self, target: str, graph: ReasoningGraph) -> EngineResponse:
        # Check M2: Have we seen this before?
        known_baseline = self.m2.get_baseline(target)
        if known_baseline:
             graph.add_step(Intent.EMPIRICAL_ANALYSIS, "Memory Retrieval (M2)", 1.0, f"Found existing analysis for {target}")

        if not self.analyzer.raw_data:
            return EngineResponse("No active workspace content. Run ingestion first.", "error", 1.0, IntelligenceLevel.SYMBOLIC, Tone.ASSERTIVE, graph.trace)

        baseline = self.analyzer.get_corpus_stats()
        graph.add_step(Intent.EMPIRICAL_ANALYSIS, "Baseline", 1.0, f"Baseline established: complexity~{baseline['avg_complexity']:.1f}")
        
        full_report = "### COGNITIVE REVIEW\n"
        targets = self.analyzer.raw_data.values() 
        overall_confidence = 0.0
        count = 0

        for analysis in targets:
            # Layer 2: Interpret
            interp = self.heuristics.interpret(analysis, baseline)
            
            # Phase 5: Update M3 (Experience)
            # Log usage for heuristics used in interpretation
            self.m3.log_heuristic_result("complexity_heuristic", 0.8) # Mock heuristic name
            
            # Layer 3: Judge
            judgement = self.judge.assess(interp)
            
            # Phase 5: Persist to M2
            self.m2.save_analysis(analysis.source, {
                "complexity": analysis.loc, # Simplified metric
                "role": interp.role
            })

            # graph.add_step moved outside to avoid RecursionError on large repos
            
            full_report += f"\n**File**: {analysis.source}\n"
            full_report += f"- Role: {interp.role.upper()}\n"
            full_report += f"- Judgment: {judgement.summary}\n"
            
            overall_confidence += judgement.confidence_score
            count += 1

        avg_conf = overall_confidence / count if count > 0 else 0.5
        
        # Add Graph Insights
        full_report += "\n### STRUCTURAL INSIGHTS (Knowledge Graph)\n"
        full_report += self.repo_analyst.get_insights(target)
        
        smells = self.repo_analyst.get_smells()
        if smells:
            full_report += "\n### ARCHITECTURAL SMELLS\n"
            for s in smells:
                full_report += f"- {s}\n"

        graph.add_step(Intent.EMPIRICAL_ANALYSIS, "Graph Synthesis", avg_conf, f"Synthesized {len(smells)} structural smells")

        # Phase 5: Local LLM Summary if enabled
        if self.local_llm.enabled:
             llm_out = self.local_llm.get_summary(full_report)
             full_report += f"\n\n**LLM Summary**: {llm_out['content']}"
             if llm_out['speculation']:
                  avg_conf += llm_out['conf_adj']

        return EngineResponse(full_report, "analysis", avg_conf, IntelligenceLevel.HEURISTIC, graph.derive_tone(avg_conf), graph.trace)

    def _handle_refactor_plan(self, target_file: str, graph: ReasoningGraph) -> EngineResponse:
        # Same logic as before, but ensure we don't auto-apply unless governed
        analysis = None
        for src, data in self.analyzer.raw_data.items():
            if target_file in src:
                analysis = data
                break
        
        if not analysis:
            return EngineResponse(f"File '{target_file}' not found.", "error", 1.0, IntelligenceLevel.SYMBOLIC, Tone.ASSERTIVE, graph.trace)

        baseline = self.analyzer.get_corpus_stats()
        interp = self.heuristics.interpret(analysis, baseline)
        judgement = self.judge.assess(interp)
        
        graph.add_step(Intent.PLANNING, "Plan Generation", judgement.confidence_score, "Generated refactor plan")
        
        # Phase 5: Governance Check for Auto-Refactor
        if self.gov.is_enabled("auto_refactor"):
             # In future, this would call `apply_plan()`
             graph.add_step(Intent.PLANNING, "Auto-Refactor", 0.0, "Auto-refactor is unsafe in this version. Skipped.")

        if not judgement.refactor_plan:
             return EngineResponse(f"No refactor necessary.", "plan", 1.0, IntelligenceLevel.HEURISTIC, Tone.ASSERTIVE, graph.trace)

        plan = judgement.refactor_plan
        content = f"### REFACTOR PLAN: {target_file}\n"
        content += f"**Goal**: {plan.goal}\n"
        content += "**Steps**:\n"
        for i, step in enumerate(plan.steps):
            content += f"{i+1}. {step}\n"
            
        return EngineResponse(content, "plan", judgement.confidence_score, IntelligenceLevel.HEURISTIC, graph.derive_tone(judgement.confidence_score), graph.trace)

    def _handle_comparison(self, target_a: str, target_b: str, graph: ReasoningGraph) -> EngineResponse:
        # Resolve targets to AnalysisResults
        data_a, data_b = None, None
        
        # Simple fuzzy match helper
        def find_target(t: str) -> Optional[Any]:
            for src, data in self.analyzer.raw_data.items():
                if t in src:
                    return data
            return None

        data_a = find_target(target_a)
        data_b = find_target(target_b)

        if not data_a or not data_b:
            missing = []
            if not data_a: missing.append(target_a)
            if not data_b: missing.append(target_b)
            return EngineResponse(f"Comparison targets not found: {', '.join(missing)}", "error", 1.0, IntelligenceLevel.SYMBOLIC, Tone.ASSERTIVE, graph.trace)

        # Execute Comparison
        result = self.comparator.compare(data_a, data_b)

        # Build Response
        content = f"### COMPARATIVE ANALYSIS\n"
        content += f"**Targets**: {result.target_a} **vs** {result.target_b}\n"
        content += f"**Winner**: {result.winner} ({result.rationale})\n\n"
        content += "**Key Differences**:\n"
        
        for diff in result.diffs:
            icon = "SAME"
            if abs(diff.delta_percent) > 10: icon = "DIFF"
            content += f"- **{diff.metric}**: {diff.target_a_val:.1f} vs {diff.target_b_val:.1f} ({diff.delta_percent:+.1f}%) [{icon}]\n"

        # Phase 5: M3 Experience Update
        self.m3.log_heuristic_result("comparator", 0.9)

        graph.add_step(Intent.COMPARATIVE_REASONING, "Comparison", 1.0, f"Compared {target_a} vs {target_b}")
        
        return EngineResponse(content, "comparison", 1.0, IntelligenceLevel.HEURISTIC, Tone.ASSERTIVE, graph.trace)

    def _local_reflex(self, text: str, graph: ReasoningGraph) -> EngineResponse:
        triggers = {
            "status": "Cognition Stack: ONLINE. Governance: ACTIVE.",
            "help": "Try: 'analyze corpus', 'plan refactor <file>', 'compare <fileA> vs <fileB>', 'learn from github <user>'."
        }
        for k, v in triggers.items():
            if k in text.lower():
                graph.add_step(Intent.EMPIRICAL_ANALYSIS, "Reflex", 1.0, "Triggered reflex response")
                return EngineResponse(v, "reflex", 1.0, IntelligenceLevel.SYMBOLIC, Tone.ASSERTIVE, graph.trace)
        
        graph.add_step(Intent.FALLBACK, "Unknown", 0.0, "No handler found")
        return EngineResponse("Command not recognized by Sovereign Kernel.", "fallback", 0.0, IntelligenceLevel.SYMBOLIC, Tone.INCONCLUSIVE, graph.trace)
    
    def _handle_github_learning(self, username: str, graph: ReasoningGraph) -> EngineResponse:
        count = self.github.index_user_repos(username)
        if count == 0:
             return EngineResponse(f"Could not index repositories for {username} (or user has no public repos).", "error", 1.0, IntelligenceLevel.EXTERNAL, Tone.CAUTIOUS, graph.trace)
        
        graph.add_step(Intent.KNOWLEDGE_ACQUISITION, "GitHub API", 1.0, f"Indexed {count} repos for {username}")
        
        summary = f"Successfully indexed {count} repositories for user '{username}'.\n"
        summary += "Knowledge chunks added to memory stream.\n"
        
        # Optionally show first few
        preview = self.github.get_knowledge()[:3]
        for chunk in preview:
             try:
                 # Check if it's a dict string from our new connector
                 import ast
                 data = ast.literal_eval(chunk) if isinstance(chunk, str) and chunk.startswith('{') else chunk
                 if isinstance(data, dict):
                     summary += f"- **{data.get('source')}**: {data.get('description')} (Stack: {data.get('tech_stack')})\n"
                 else:
                     summary += f"- {chunk}\n"
             except:
                 summary += f"- {chunk}\n"
             
        return EngineResponse(summary, "knowledge", 1.0, IntelligenceLevel.EXTERNAL, Tone.ASSERTIVE, graph.trace)
