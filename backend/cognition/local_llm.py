
import os
import requests
from typing import Dict, Any, Optional

class LocalLLMConnector:
    """
    PHASE 5: LOCAL LLM (Sandboxed)
    Wraps local inference server API (Ollama/llama.cpp compatible).
    """
    def __init__(self, endpoint: str = None, enabled: bool = False):
        # Default to Ollama (11434) or user provided
        self.endpoint = endpoint or os.getenv("PRIMERS_LLM_ENDPOINT", "http://localhost:11434/v1/chat/completions")
        self.enabled = enabled
        self.model = os.getenv("PRIMERS_LLM_MODEL", "llama3") # Default model

    def get_summary(self, context: str) -> Dict[str, Any]:
        """
        Request a natural language summary. Strictly read-only context.
        """
        if not self.enabled:
            return {"content": "[LLM DISABLED]", "speculation": False, "conf_adj": 0.0}

        prompt = f"You are an objective code analyst. Summarize this analysis briefly.\nContext: {context}"
        
        try:
            content = self._call_llm(prompt)
            if content:
                return {"content": content, "speculation": True, "conf_adj": 0.05}
        except Exception as e:
            print(f"LLM Error: {e}")
            
        # Fallback if connection fails
        return {
            "content": "(Local LLM Offline - Simulation): The code structure suggests a nascent plugin architecture.", 
            "speculation": True, 
            "conf_adj": -0.05
        }

    def chat(self, message: str, history: List[Dict[str, str]] = None) -> str:
        """
        General conversational capability for the 'FALLBACK' intent.
        Includes history for multi-turn chat.
        """
        if not self.enabled:
            return "Cognitive Core: Interaction restricted to command syntax only. Enable 'local_llm' for conversation."

        system_prompt = (
            "You are Primers S-Form, a Sovereign AI Cognitive Engine. "
            "Your personality is objective, technically precise, and assertive. "
            "You focus on code architecture, structural intelligence, and refactoring logic. "
            "Do not use generic assistant greetings. Speak as a kernel process."
        )

        try:
            response = self._call_llm(message, history=history, system_prompt=system_prompt)
            if response:
                return response
        except Exception as e:
            print(f"LLM Chat Error: {e}")

        # 🧠 SYMBOLIC INTELLIGENCE (LLM-OFFLINE REASONING)
        query = message.lower()
        
        # Knowledge about S-Form
        if any(k in query for k in ["what is", "who are you", "primers intelligence"]):
            return (
                "## Primers Intelligence\n"
                "I am a specialized Intelligence Engine for Code Architecture. My core is built upon a **3-Layer Cognitive Stack**:\n\n"
                "1. **Analysis (Layer 1)**: AST-based parsing for exact structural mapping.\n"
                "2. **Interpretation (Layer 2)**: Heuristics for role discovery (God Objects, Workers).\n"
                "3. **Judgment (Layer 3)**: Risk assessment and Refactor evaluaton.\n\n"
                "I am currently operating in **High-Fidelity Symbolic Mode**."
            )

        if "cognitive stack" in query or "layers" in query:
            return (
                "### Cognitive Stack Specification\n"
                "- **Layer 1 (Analyzer)**: Generates AST nodes and calculates LOC/Complexity.\n"
                "- **Layer 2 (Heuristics)**: Identifies patterns like 'God Objects' or 'God Functions'.\n"
                "- **Layer 3 (Judge)**: Calibrates confidence and provides the Sovereign Verdict."
            )

        # 3. Dynamic Knowledge (Using context if we were to pass it)
        if "analyze" in query or "review" in query:
             return "To perform deep analysis, please use the `analyze corpus` command. This triggers my Layer 2 heuristic interpretation across all ingested files."

        if "github" in query:
             return "My acquisition layer allows for direct GitHub indexing. Syntax: `learn from github <username>`. This appends repository metadata to my factual memory (M2)."

        # 4. Contextual Fallback
        return (
            f"### SYSTEM REFLEX: {message.upper()}\n"
            "My local inference server (Ollama) is currently unreachable. However, I have processed your input through my **Symbolic Interpretation Layer**.\n\n"
            "**Verdict**: Input detected as general query. \n"
            "**Action**: Providing technical system context based on internal architectural schemas.\n\n"
            "*Technical Note: To unlock full non-technical conversation, ensure a local LLM is running at the configured endpoint.*"
        )

    def _call_llm(self, user_message: str, history: List[Dict[str, str]] = None, system_prompt: str = None) -> Optional[str]:
        headers = {"Content-Type": "application/json"}
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if history:
            messages.extend(history)
            # If the last message in history is from the user, replace it with the enriched one
            if messages and messages[-1]['role'] == 'user':
                messages[-1]['content'] = user_message
        else:
            messages.append({"role": "user", "content": user_message})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "temperature": 0.5
        }

        try:
            # tailored for OpenAI compatible API (Ollama v1)
            res = requests.post(self.endpoint, json=payload, headers=headers, timeout=15)
            if res.status_code == 200:
                data = res.json()
                return data['choices'][0]['message']['content']
        except Exception:
            raise
        
        return None
