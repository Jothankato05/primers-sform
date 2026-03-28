
import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface RescueDashboardProps {
  onCommand: (msg: string) => void;
  status: any;
}

const RescueDashboard: React.FC<RescueDashboardProps> = ({ onCommand, status }) => {
  const [triageText, setTriageText] = useState("");

  const cardVariants = {
    hover: { scale: 1.02, transition: { duration: 0.2 } },
    tap: { scale: 0.98 }
  };

  return (
    <div className="rescue-container">
      <header className="rescue-header">
        <h2 className="rescue-title">SecureLink SOS Matrix</h2>
        <div className="status-grid">
          {Object.entries(status || {}).map(([name, state]) => (
            <div key={name} className={`status-pill ${state === 'READY' ? 'ready' : 'simulated'}`}>
              <span className="pill-name">{name.replace('_', ' ').toUpperCase()}</span>
              <span className="pill-dot"></span>
              <span className="pill-state">{state as string}</span>
            </div>
          ))}
        </div>
      </header>

      <div className="rescue-grid">
        {/* BERT Triage */}
        <motion.div className="rescue-card triage" variants={cardVariants} whileHover="hover" whileTap="tap">
          <div className="card-icon">⚡</div>
          <h3>Emergency Triage (BERT)</h3>
          <p>Classify distress signals and prioritize victims.</p>
          <textarea 
            placeholder="Enter situation report..." 
            value={triageText}
            onChange={(e) => setTriageText(e.target.value)}
          />
          <button onClick={() => onCommand(`triage ${triageText}`)}>RUN TRIAGE</button>
        </motion.div>

        {/* DAN-Qwen Logic */}
        <motion.div className="rescue-card logic" variants={cardVariants} whileHover="hover" whileTap="tap">
          <div className="card-icon">🧠</div>
          <h3>Rescue Logic (DAN-Qwen)</h3>
          <p>Generate autonomous rescue protocols and medical steps.</p>
          <button onClick={() => onCommand("rescue generate protocol")}>GENERATE PROTOCOL</button>
        </motion.div>

        {/* DETR Witness */}
        <motion.div className="rescue-card witness" variants={cardVariants} whileHover="hover" whileTap="tap">
          <div className="card-icon">👁️</div>
          <h3>Image Witness (DETR)</h3>
          <p>Scan visual feeds for threat detection and victim localization.</p>
          <button onClick={() => onCommand("witness scan image")}>RUN VISION SCAN</button>
        </motion.div>

        {/* Whisper Guardian */}
        <motion.div className="rescue-card audio" variants={cardVariants} whileHover="hover" whileTap="tap">
          <div className="card-icon">🎙️</div>
          <h3>Voice Guardian (Whisper)</h3>
          <p>Live transcription of distress calls for NLP analysis.</p>
          <button onClick={() => onCommand("audio transcribe")}>START LISTENING</button>
        </motion.div>
      </div>

      <style>{`
        .rescue-container {
          padding: 2rem;
          background: rgba(14, 14, 20, 0.8);
          border-radius: 20px;
          border: 1px solid rgba(255, 60, 60, 0.2);
          backdrop-filter: blur(20px);
          color: white;
        }
        .rescue-header {
          margin-bottom: 2rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
          padding-bottom: 1rem;
        }
        .rescue-title {
          font-size: 1.8rem;
          font-weight: 800;
          color: #ff3c3c;
          text-transform: uppercase;
          letter-spacing: 2px;
          margin: 0;
        }
        .status-grid {
          display: flex;
          gap: 1rem;
        }
        .status-pill {
          background: rgba(255, 255, 255, 0.05);
          padding: 0.4rem 0.8rem;
          border-radius: 99px;
          font-size: 0.7rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .status-pill.ready { border-color: #00ff88; color: #00ff88; }
        .status-pill.simulated { border-color: #ffcc00; color: #ffcc00; }
        .pill-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }

        .rescue-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 1.5rem;
        }
        .rescue-card {
           background: rgba(255, 255, 255, 0.03);
           padding: 1.5rem;
           border-radius: 16px;
           border: 1px solid rgba(255, 255, 255, 0.08);
           display: flex;
           flex-direction: column;
           gap: 1rem;
        }
        .card-icon { font-size: 2.2rem; }
        .rescue-card h3 { margin: 0; font-size: 1.2rem; color: #fff; }
        .rescue-card p { font-size: 0.9rem; color: #aaa; margin: 0; line-height: 1.4; }
        
        textarea {
          background: rgba(0, 0, 0, 0.3);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 8px;
          padding: 0.8rem;
          color: white;
          font-family: inherit;
          min-height: 80px;
          resize: none;
        }

        button {
          background: #ff3c3c;
          color: white;
          border: none;
          padding: 0.8rem;
          border-radius: 8px;
          font-weight: 700;
          cursor: pointer;
          transition: 0.2s;
          text-transform: uppercase;
          font-size: 0.8rem;
          letter-spacing: 1px;
        }
        button:hover {
          background: #ff5555;
          box-shadow: 0 0 20px rgba(255, 60, 60, 0.4);
        }
        .triage { border-left: 4px solid #ff3c3c; }
        .logic { border-left: 4px solid #3c8cff; }
        .witness { border-left: 4px solid #cc00ff; }
        .audio { border-left: 4px solid #00ffcc; }
      `}</style>
    </div>
  );
};

export default RescueDashboard;
