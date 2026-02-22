import React, { useMemo } from 'react';
import { motion } from 'framer-motion';

interface AvatarProps {
    isTyping: boolean;
    isResponding: boolean;
    mousePos: { x: number; y: number };
}

const Avatar: React.FC<AvatarProps> = ({ isTyping, isResponding, mousePos }) => {
    // Parallax logic
    const springProps = { type: "spring", stiffness: 150, damping: 15, mass: 0.8 } as const;

    const parallax = useMemo(() => {
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;
        const dx = (mousePos.x - centerX) / (centerX || 1);
        const dy = (mousePos.y - centerY) / (centerY || 1);

        return {
            head: { x: dx * 4, y: dy * 4, rotateX: -dy * 10, rotateY: dx * 10 },
            eyes: { x: dx * 8, y: dy * 8 },
            pupils: { x: dx * 4, y: dy * 4 }
        };
    }, [mousePos]);

    const mouthPaths = {
        idle: "M35 75 Q 50 76 65 75",
        thinking: "M40 75 Q 50 75 60 75",
        speaking: "M30 75 Q 50 85 70 75"
    };

    return (
        <div className="avatar-wrapper" style={{ perspective: '1000px' }}>
            <motion.svg
                viewBox="0 0 100 100"
                className="avatar-svg"
                initial={false}
                animate={parallax.head}
                transition={springProps}
            >
                <defs>
                    <filter id="celestial-glow" x="-50%" y="-50%" width="200%" height="200%">
                        <feGaussianBlur stdDeviation="2.5" result="blur" />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>

                    <radialGradient id="soulGradient" cx="50%" cy="40%" r="60%">
                        <stop offset="0%" stopColor="#2a2a2a" />
                        <stop offset="70%" stopColor="#0a0a0a" />
                        <stop offset="100%" stopColor="#000000" />
                    </radialGradient>

                    <linearGradient id="auraGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="rgba(255,255,255,0.05)" />
                        <stop offset="50%" stopColor="rgba(255,255,255,0.15)" />
                        <stop offset="100%" stopColor="rgba(255,255,255,0.05)" />
                    </linearGradient>
                </defs>

                {/* Ethereal Halo - Active during Thinking/Responding */}
                <motion.circle
                    cx="50" cy="50" r="45"
                    fill="none"
                    stroke="url(#auraGradient)"
                    strokeWidth="0.3"
                    animate={{
                        rotate: 360,
                        scale: isResponding ? [1, 1.05, 1] : 1,
                        opacity: isTyping || isResponding ? 0.6 : 0.2
                    }}
                    transition={{
                        rotate: { duration: 10, repeat: Infinity, ease: "linear" },
                        scale: { duration: 2, repeat: Infinity }
                    }}
                />

                {/* Main Head Structure */}
                <motion.g style={{ filter: 'drop-shadow(0 0 10px rgba(0,0,0,0.5))' }}>
                    <path
                        d="M50 10 C 20 10 15 40 15 60 C 15 85 35 95 50 95 C 65 95 85 85 85 60 C 85 40 80 10 50 10"
                        fill="url(#soulGradient)"
                        stroke="rgba(255, 255, 255, 0.08)"
                        strokeWidth="0.5"
                    />
                </motion.g>

                {/* Sensory Cluster (Eyes) */}
                <motion.g animate={parallax.eyes} transition={springProps}>
                    {/* Left Eye */}
                    <g transform="translate(35, 45)">
                        <circle r="8" fill="rgba(0,0,0,0.6)" />
                        <motion.circle
                            r={isTyping ? 1.5 : 3}
                            fill="#d4d4d8"
                            animate={parallax.pupils}
                            style={{ filter: 'url(#celestial-glow)' }}
                            transition={springProps}
                        />
                    </g>

                    {/* Right Eye */}
                    <g transform="translate(65, 45)">
                        <circle r="8" fill="rgba(0,0,0,0.6)" />
                        <motion.circle
                            r={isTyping ? 1.5 : 3}
                            fill="#d4d4d8"
                            animate={parallax.pupils}
                            style={{ filter: 'url(#celestial-glow)' }}
                            transition={springProps}
                        />
                    </g>
                </motion.g>

                {/* Cognitive Interface (Mouth/Rift) */}
                <motion.path
                    d={isResponding ? mouthPaths.speaking : isTyping ? mouthPaths.thinking : mouthPaths.idle}
                    fill="none"
                    stroke={isResponding ? "#ffffff" : "rgba(255,255,255,0.2)"}
                    strokeWidth={isResponding ? 1.5 : 0.8}
                    strokeLinecap="round"
                    animate={{
                        d: isResponding ? mouthPaths.speaking : isTyping ? mouthPaths.thinking : mouthPaths.idle,
                        opacity: isResponding ? [0.6, 1, 0.6] : 1
                    }}
                    transition={{
                        d: { duration: 0.4, ease: "anticipate" },
                        opacity: { duration: 1.5, repeat: Infinity }
                    }}
                />

                {/* Thinking Gesture - High Fidelity */}
                <motion.g
                    initial={{ y: 50, opacity: 0 }}
                    animate={{
                        y: isTyping ? 0 : 50,
                        opacity: isTyping ? 0.8 : 0,
                        x: parallax.head.x * 0.5
                    }}
                    transition={springProps}
                >
                    <path d="M40 100 Q 50 92 60 100" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="1.5" />
                    <motion.path
                        d="M50 96 L 50 82"
                        stroke="#fff"
                        strokeWidth="1.2"
                        strokeLinecap="round"
                        animate={{ y: [0, -2, 0] }}
                        transition={{ duration: 2, repeat: Infinity }}
                    />
                    <path d="M44 98 L 42 88" stroke="rgba(255,255,255,0.3)" strokeWidth="1" strokeLinecap="round" />
                    <path d="M56 98 L 58 88" stroke="rgba(255,255,255,0.3)" strokeWidth="1" strokeLinecap="round" />
                </motion.g>

                {/* Ambient Vitality (Particles) */}
                {[...Array(5)].map((_, i) => (
                    <motion.circle
                        key={i}
                        r="0.4"
                        fill="#fff"
                        initial={{ x: Math.random() * 100, y: Math.random() * 100, opacity: 0 }}
                        animate={{
                            y: [null, Math.random() * -20],
                            opacity: [0, 0.4, 0]
                        }}
                        transition={{
                            duration: 3 + Math.random() * 4,
                            repeat: Infinity,
                            delay: Math.random() * i
                        }}
                    />
                ))}
            </motion.svg>
        </div>
    );
};

export default Avatar;
