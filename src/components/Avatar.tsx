import React, { useEffect, useState, useRef } from 'react';

interface AvatarProps {
    isTyping: boolean;
    isResponding: boolean;
    mousePos: { x: number; y: number };
}

const Avatar: React.FC<AvatarProps> = ({ isTyping, isResponding, mousePos }) => {
    const [eyeOffset, setEyeOffset] = useState({ x: 0, y: 0 });
    const [mouthPath, setMouthPath] = useState("M35 75 Q 50 75 65 75");
    const requestRef = useRef<number>(null);

    useEffect(() => {
        // Tracking calculation with a more "visceral" weight
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;

        const limit = isTyping ? 2 : 6;
        const dx = (mousePos.x - centerX) / centerX;
        const dy = (mousePos.y - centerY) / centerY;

        setEyeOffset({
            x: dx * limit,
            y: dy * limit
        });
    }, [mousePos, isTyping]);

    useEffect(() => {
        // Organic Mouth Animation (The Living God)
        let frame = 0;
        const animate = () => {
            if (isResponding) {
                const openness = 5 + Math.sin(frame * 0.2) * 8;
                const width = 30 + Math.sin(frame * 0.1) * 5;
                const x1 = 50 - width / 2;
                const x2 = 50 + width / 2;
                const controlY = 75 + openness;

                setMouthPath(`M${x1} 75 Q 50 ${controlY} ${x2} 75`);
                frame++;
                requestRef.current = requestAnimationFrame(animate);
            } else {
                setMouthPath("M35 75 Q 50 76 65 75");
            }
        };

        if (isResponding) {
            animate();
        } else {
            setMouthPath("M35 75 Q 50 75.5 65 75");
        }

        return () => {
            if (requestRef.current) cancelAnimationFrame(requestRef.current);
        };
    }, [isResponding]);

    return (
        <div className={`avatar-container ${isTyping ? 'concentrating' : ''}`}>
            <svg viewBox="0 0 100 100" className="avatar-svg">
                <defs>
                    <filter id="celestial-glow">
                        <feGaussianBlur stdDeviation="3" result="blur">
                            <animate attributeName="stdDeviation" values="2;4;2" dur="4s" repeatCount="indefinite" />
                        </feGaussianBlur>
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>

                    <radialGradient id="faceGradient" cx="50%" cy="40%" r="60%">
                        <stop offset="0%" stopColor="#262626" />
                        <stop offset="70%" stopColor="#0a0a0a" />
                        <stop offset="100%" stopColor="#000000" />
                    </radialGradient>

                    <filter id="texture">
                        <feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves="3" result="noise" />
                        <feDisplacementMap in="SourceGraphic" in2="noise" scale="2" />
                    </filter>
                </defs>

                {/* The Head - Ethereal Matte Surface */}
                <g filter="url(#texture)">
                    <path
                        d="M50 10 C 20 10 15 40 15 60 C 15 85 35 95 50 95 C 65 95 85 85 85 60 C 85 40 80 10 50 10"
                        fill="url(#faceGradient)"
                        stroke="rgba(255, 255, 255, 0.05)"
                        strokeWidth="0.5"
                    />
                </g>

                {/* Celestial Eyes - Neutral Light */}
                <g transform={`translate(${eyeOffset.x}, ${eyeOffset.y})`}>
                    {/* Left Socket */}
                    <ellipse cx="35" cy="45" rx="8" ry="10" fill="rgba(0,0,0,0.8)" />
                    {/* Left Iris */}
                    <circle cx="35" cy="45" r={isTyping ? "1.5" : "3"} fill="#a3a3a3" filter="url(#celestial-glow)">
                        <animate attributeName="r" values="2.5;3;2.5" dur="4s" repeatCount="indefinite" />
                    </circle>

                    {/* Right Socket */}
                    <ellipse cx="65" cy="45" rx="8" ry="10" fill="rgba(0,0,0,0.8)" />
                    {/* Right Iris */}
                    <circle cx="65" cy="45" r={isTyping ? "1.5" : "3"} fill="#a3a3a3" filter="url(#celestial-glow)">
                        <animate attributeName="r" values="2.5;3;2.5" dur="4s" repeatCount="indefinite" />
                    </circle>
                </g>

                {/* Brow Lines */}
                <path
                    d="M25 35 Q 35 30 43 38"
                    fill="none"
                    stroke="rgba(255,255,255,0.05)"
                    strokeWidth="0.5"
                    style={{ transform: `translateY(${isTyping ? 2 : 0}px)` }}
                />
                <path
                    d="M75 35 Q 65 30 57 38"
                    fill="none"
                    stroke="rgba(255,255,255,0.05)"
                    strokeWidth="0.5"
                    style={{ transform: `translateY(${isTyping ? 2 : 0}px)` }}
                />

                {/* Speaking Rift */}
                <path
                    d={mouthPath}
                    fill="none"
                    stroke={isResponding ? "rgba(255, 255, 255, 0.4)" : "rgba(255,255,255,0.1)"}
                    strokeWidth={isResponding ? 1 : 0.5}
                    filter={isResponding ? "url(#celestial-glow)" : "none"}
                    strokeLinecap="round"
                />

                {/* Thinking Gesture - Ethereal Hand */}
                <g
                    style={{
                        transition: 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)',
                        transform: `translateY(${isTyping ? -15 : 40}px) translateX(${eyeOffset.x * 0.8}px)`,
                        opacity: isTyping ? 0.6 : 0
                    }}
                >
                    {/* Palm/Base */}
                    <path d="M40 105 Q 50 95 60 105" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="2" />
                    {/* Fingers in Thinking Posture */}
                    <path d="M43 100 L 41 88" stroke="rgba(255,255,255,0.2)" strokeWidth="1" strokeLinecap="round" />
                    <path d="M50 98 L 50 82" stroke="rgba(255,255,255,0.4)" strokeWidth="1.2" strokeLinecap="round" filter="url(#celestial-glow)" />
                    <path d="M57 100 L 59 88" stroke="rgba(255,255,255,0.2)" strokeWidth="1" strokeLinecap="round" />
                </g>

                {/* Ambient Particles */}
                <g opacity="0.4">
                    <circle cx="20" cy="20" r="0.5" fill="#fff"><animate attributeName="opacity" values="0;1;0" dur="3s" repeatCount="indefinite" /></circle>
                    <circle cx="80" cy="30" r="0.3" fill="#fff"><animate attributeName="opacity" values="0;1;0" dur="5s" repeatCount="indefinite" /></circle>
                    <circle cx="50" cy="85" r="0.4" fill="#fff"><animate attributeName="opacity" values="0;1;0" dur="4s" repeatCount="indefinite" /></circle>
                </g>
            </svg>
        </div>
    );
};

export default Avatar;
