import React from 'react';

interface DiffViewerProps {
    oldCode: string;
    newCode: string;
    fileName: string;
}

const DiffViewer: React.FC<DiffViewerProps> = ({ oldCode, newCode, fileName }) => {
    const oldLines = oldCode.split('\n');
    const newLines = newCode.split('\n');

    return (
        <div className="diff-viewer">
            <div className="diff-header">
                <span>Architectural Refactor Preview: {fileName}</span>
            </div>
            <div className="diff-grid">
                <div className="diff-column">
                    <div className="column-label">Current Strategy</div>
                    <div className="code-container">
                        {oldLines.map((line, i) => (
                            <div key={i} className="code-line">
                                <span className="line-number">{i + 1}</span>
                                <span className="line-content">{line || ' '}</span>
                            </div>
                        ))}
                    </div>
                </div>
                <div className="diff-column">
                    <div className="column-label">Proposed Optimization</div>
                    <div className="code-container">
                        {newLines.map((line, i) => {
                            const isNew = !oldLines.includes(line);
                            return (
                                <div key={i} className={`code-line ${isNew ? 'line-added' : ''}`}>
                                    <span className="line-number">{i + 1}</span>
                                    <span className="line-content">{line || ' '}</span>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DiffViewer;
