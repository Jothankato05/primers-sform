import { useState, useEffect, useRef } from 'react'
import './App.css'



interface ReasoningStep {
  step_id: string;
  intent: string;
  action: string;
  confidence: number;
  output_summary: string;
}

interface EngineResponse {
  content: string;
  intent: string;
  confidence: number;
  level: string;
  tone: string;
  trace: ReasoningStep[];
  meta: any;
}

interface Message {
  id: string;
  role: 'user' | 'system';
  content: string;
  trace?: ReasoningStep[];
  level?: string;
  tone?: string;
  confidence?: number;
}

const API_URL = "http://localhost:8000";

function App() {
  const [messages, setMessages] = useState<Message[]>([
    { id: 'init', role: 'system', content: 'PrimersGPT System Online. version 3.0.0 (Phase 5)' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const send = async () => {
    if (!input.trim()) return;
    const userMsg: Message = { id: Date.now().toString(), role: 'user', content: input };
    setMessages(p => [...p, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg.content })
      });
      const data = await res.json();
      const engineRes: EngineResponse = data.response;

      setMessages(p => [...p, {
        id: Date.now().toString(),
        role: 'system',
        content: engineRes.content,
        trace: engineRes.trace,
        level: engineRes.level,
        tone: engineRes.tone,
        confidence: engineRes.confidence
      }]);
    } catch (e) {
      setMessages(p => [...p, { id: Date.now().toString(), role: 'system', content: 'CONNECTION ERROR: Backend unreachable.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleIngest = async () => {
    const user = prompt("GitHub Username for Knowledge Graph:");
    if (!user) return;
    setMessages(p => [...p, { id: 'sys', role: 'system', content: `Creating ingestion task for user: ${user}...` }]);

    try {
      const res = await fetch(`${API_URL}/ingest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target: 'github', params: { username: user } })
      });
      const data = await res.json();
      setMessages(p => [...p, { id: Date.now().toString(), role: 'system', content: data.message }]);
    } catch (e) {
      setMessages(p => [...p, { id: 'err', role: 'system', content: 'Ingestion Failed.' }]);
    }
  };

  return (
    <div className="layout">
      <div className="bg-grid"></div>

      {/* Sidebar */}
      <aside className="sidebar">
        <div className="brand">
          <img src="/logo.jpg" className="brand-logo" alt="" />
          <div className="brand-text">
            <h1>PRIMERS</h1>
            <span className="subtitle">INTELLIGENCE</span>
          </div>
        </div>

        <div className="nav-menu">
          <div className="nav-item active">
            <img src="/node_icon.png" className="icon" /> Neural Core
          </div>
          <div className="nav-item" onClick={handleIngest}>
            <img src="/node_icon.png" className="icon" /> Ingest Data
          </div>
        </div>

        <div className="sys-status">
          <div className="stat-row">
            <span>CPU</span>
            <div className="bar"><div className="fill" style={{ width: '24%' }}></div></div>
          </div>
          <div className="stat-row">
            <span>MEM</span>
            <div className="bar"><div className="fill" style={{ width: '41%' }}></div></div>
          </div>
        </div>
      </aside>

      {/* Main Terminal */}
      <main className="main-view">
        <div className="chat-window">
          {messages.map(m => (
            <div key={m.id} className={`msg-row ${m.role}`}>
              <div className="msg-content">
                <div className="msg-header">
                  <span className="sender">{m.role === 'user' ? 'USR' : 'SYS'} //</span>
                  {m.tone && <span className={`tone-badge ${m.tone}`}>{m.tone.toUpperCase()}</span>}
                  {m.confidence && <span className="conf-badge">CONF: {m.confidence.toFixed(2)}</span>}
                </div>

                <div className="msg-text">{m.content}</div>

                {/* Trace Display */}
                {m.trace && m.trace.length > 0 && (
                  <div className="trace-box">
                    <div className="trace-header">REASONING GRAPH [{m.level || 'Unknown'}]</div>
                    {m.trace.map((t) => (
                      <div key={t.step_id} className="trace-line">
                        <span className="trace-intent">[{t.intent}]</span>
                        <span className="trace-action">{t.action}</span>
                        <span className="trace-summary">: {t.output_summary}</span>
                        <span className="trace-conf">({t.confidence.toFixed(2)})</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && <div className="msg-row system"><div className="msg-content">PROCESSING...</div></div>}
          <div ref={endRef} />
        </div>

        <div className="input-deck">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && send()}
            placeholder="ENTER COMMAND (e.g. 'review repo', 'analyze core')..."
          />
        </div>
      </main>
    </div>
  )
}

export default App
