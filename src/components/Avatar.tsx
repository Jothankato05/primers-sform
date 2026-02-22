import React, { useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface AvatarProps {
    isTyping: boolean;
    isResponding: boolean;
    mousePos: { x: number; y: number };
    isIdle?: boolean;
}

const Avatar: React.FC<AvatarProps> = ({ isTyping, isResponding, mousePos, isIdle }) => {
    // Parallax logic
    const springProps = { type: "spring", stiffness: 150, damping: 15, mass: 0.8 } as const;

    // Idle Sovereignty: The Avatar performs "background work" when user is away
    const isWorking = isIdle && !isTyping && !isResponding;

    const parallax = useMemo(() => {
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;
        const dx = (mousePos.x - centerX) / (centerX || 1);
        const dy = (mousePos.y - centerY) / (centerY || 1);

        // When idling, look slightly upward or at the "hacking" data
        const targetX = isWorking ? 0 : dx;
        const targetY = isWorking ? -0.2 : dy;

        return {
            head: { x: targetX * 4, y: targetY * 4, rotateX: -targetY * 10, rotateY: targetX * 10 },
            eyes: { x: targetX * 8, y: targetY * 8 },
            pupils: { x: targetX * 4, y: targetY * 4 }
        };
    }, [mousePos, isWorking]);

    const mouthPaths = {
        idle: "M35 75 Q 50 76 65 75",
        thinking: "M40 75 Q 50 75 60 75",
        speaking: "M30 75 Q 50 85 70 75",
        hacking: "M42 75 Q 50 73 58 75" // Concentrated thin line
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

                    <filter id="glitch">
                        <feOffset in="SourceGraphic" dx="1" dy="0" result="offset1" />
                        <feOffset in="SourceGraphic" dx="-1" dy="0" result="offset2" />
                        <feBlend in="offset1" in2="offset2" mode="screen" />
                    </filter>
                </defs>

                {/* Hacking Particles / Matrix Grid Overlay during Idle */}
                <AnimatePresence>
                    {isWorking && (
                        <motion.g
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 0.3 }}
                            exit={{ opacity: 0 }}
                        >
                            {[...Array(6)].map((_, i) => (
                                <motion.rect
                                    key={i}
                                    x={15 + i * 12}
                                    y="10"
                                    width="0.5"
                                    height="80"
                                    fill="rgba(255,255,255,0.1)"
                                    animate={{
                                        opacity: [0.1, 0.4, 0.1],
                                        y: [10, 20, 10]
                                    }}
                                    transition={{ duration: 2, repeat: Infinity, delay: i * 0.3 }}
                                />
                            ))}
                        </motion.g>
                    )}
                </AnimatePresence>

                {/* Ethereal Halo */}
                <motion.circle
                    cx="50" cy="50" r="45"
                    fill="none"
                    stroke="url(#auraGradient)"
                    strokeWidth="0.3"
                    animate={{
                        rotate: 360,
                        scale: (isResponding || isWorking) ? [1, 1.05, 1] : 1,
                        opacity: (isTyping || isResponding || isWorking) ? 0.6 : 0.2
                    }}
                    transition={{
                        rotate: { duration: 10, repeat: Infinity, ease: "linear" },
                        scale: { duration: 2, repeat: Infinity }
                    }}
                />

                {/* Main Head Structure */}
                <motion.g
                    style={{ filter: 'drop-shadow(0 0 10px rgba(0,0,0,0.5))' }}
                    animate={isWorking ? { filter: ['drop-shadow(0 0 10px rgba(0,0,0,0.5))', 'drop-shadow(0 0 15px rgba(255,255,255,0.1))', 'drop-shadow(0 0 10px rgba(0,0,0,0.5))'] } : {}}
                    transition={{ duration: 3, repeat: Infinity }}
                >
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
                            r={isTyping ? 1.5 : (isWorking ? 2 : 3)}
                            fill={isWorking ? "#fff" : "#d4d4d8"}
                            animate={parallax.pupils}
                            style={{ filter: 'url(#celestial-glow)' }}
                            transition={springProps}
                        />
                    </g>

                    {/* Right Eye */}
                    <g transform="translate(65, 45)">
                        <circle r="8" fill="rgba(0,0,0,0.6)" />
                        <motion.circle
                            r={isTyping ? 1.5 : (isWorking ? 2 : 3)}
                            fill={isWorking ? "#fff" : "#d4d4d8"}
                            animate={parallax.pupils}
                            style={{ filter: 'url(#celestial-glow)' }}
                            transition={springProps}
                        />
                    </g>
                </motion.g>

                {/* Cognitive Interface (Mouth/Rift) */}
                <motion.path
                    d={isResponding ? mouthPaths.speaking : (isWorking ? mouthPaths.hacking : (isTyping ? mouthPaths.thinking : mouthPaths.idle))}
                    fill="none"
                    stroke={(isResponding || isWorking) ? "#ffffff" : "rgba(255,255,255,0.2)"}
                    strokeWidth={(isResponding || isWorking) ? 1.5 : 0.8}
                    strokeLinecap="round"
                    animate={{
                        d: isResponding ? mouthPaths.speaking : (isWorking ? mouthPaths.hacking : (isTyping ? mouthPaths.thinking : mouthPaths.idle)),
                        opacity: (isResponding || isWorking) ? [0.6, 1, 0.6] : 1
                    }}
                    transition={{
                        d: { duration: 0.4, ease: "anticipate" },
                        opacity: { duration: 1.5, repeat: Infinity }
                    }}
                />

                {/* Thinking/Working Gesture */}
                <motion.g
                    initial={{ y: 50, opacity: 0 }}
                    animate={{
                        y: (isTyping || isWorking) ? 0 : 50,
                        opacity: (isTyping || isWorking) ? 0.8 : 0,
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
                        animate={isWorking ? { y: [-1, 2, -1], rotate: [0, 5, -5, 0] } : { y: [0, -2, 0] }}
                        transition={{ duration: 2, repeat: Infinity }}
                    />
                    <path d="M44 98 L 42 88" stroke="rgba(255,255,255,0.3)" strokeWidth="1" strokeLinecap="round" />
                    <path d="M56 98 L 58 88" stroke="rgba(255,255,255,0.3)" strokeWidth="1" strokeLinecap="round" />
                </motion.g>

                {/* Hacking Data Glyphs when Idling */}
                <AnimatePresence>
                    {isWorking && (
                        <motion.g
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                        >
                            <motion.text
                                x="50" y="25"
                                fontSize="2"
                                fill="#fff"
                                textAnchor="middle"
                                style={{ fontFamily: 'monospace', filter: 'url(#celestial-glow)', opacity: 0.4 }}
                                animate={{ opacity: [0.2, 0.6, 0.2] }}
                                transition={{ duration: 1.5, repeat: Infinity }}
                            >
                                SYSTEM_OPTIMIZING...
                            </motion.text>
                            <motion.path
                                d="M30 30 L 70 30"
                                stroke="rgba(255,255,255,0.2)"
                                strokeWidth="0.2"
                                animate={{ scaleX: [0, 1, 0], x: [0, 0, 0] }}
                                transition={{ duration: 4, repeat: Infinity }}
                            />
                        </motion.g>
                    )}
                </AnimatePresence>

                {/* Ambient Vitality */}
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
