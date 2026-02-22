import React, { useMemo, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface AvatarProps {
    isTyping: boolean;
    isResponding: boolean;
    mousePos: { x: number; y: number };
    isIdle?: boolean;
}

const Avatar: React.FC<AvatarProps> = ({ isTyping, isResponding, mousePos, isIdle }) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const springProps = { type: "spring", stiffness: 150, damping: 15, mass: 0.8 } as const;
    const isWorking = isIdle && !isTyping && !isResponding;

    // High-performance "Quantum Hacking" Canvas Animation
    useEffect(() => {
        if (!isWorking || !canvasRef.current) return;

        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationFrame: number;
        const particles: any[] = [];
        const codeSnips = ["def audit():", "mem_alloc", "ptr->0x7f", "std::move", "async {", "011010", "node.relink()"];

        const resize = () => {
            canvas.width = 160;
            canvas.height = 160;
        };
        resize();

        class HackingParticle {
            x: number; y: number; speed: number; char: string; opacity: number;
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.speed = 0.5 + Math.random() * 2;
                this.char = codeSnips[Math.floor(Math.random() * codeSnips.length)];
                this.opacity = 0;
            }
            draw() {
                if (!ctx) return;
                ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity})`;
                ctx.font = '6px monospace';
                ctx.fillText(this.char, this.x, this.y);
                this.y -= this.speed;
                this.opacity = Math.sin(Date.now() * 0.005 + this.x) * 0.3;
                if (this.y < -10) { this.y = canvas.height + 10; this.x = Math.random() * canvas.width; }
            }
        }

        for (let i = 0; i < 15; i++) particles.push(new HackingParticle());

        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => p.draw());
            animationFrame = requestAnimationFrame(animate);
        };
        animate();

        return () => cancelAnimationFrame(animationFrame);
    }, [isWorking]);

    const parallax = useMemo(() => {
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;
        const dx = (mousePos.x - centerX) / (centerX || 1);
        const dy = (mousePos.y - centerY) / (centerY || 1);

        const targetX = isWorking ? Math.sin(Date.now() * 0.001) * 0.05 : dx;
        const targetY = isWorking ? -0.1 : dy;

        return {
            head: { x: targetX * 4, y: targetY * 4, rotateX: -targetY * 10, rotateY: targetX * 10 },
            eyes: { x: targetX * 8, y: targetY * 8 },
            pupils: { x: targetX * 4, y: targetY * 4 }
        };
    }, [mousePos, isWorking]);

    return (
        <div className="avatar-wrapper" style={{ perspective: '1000px', position: 'relative' }}>
            {/* Background Data Rain (Canvas) */}
            <canvas
                ref={canvasRef}
                style={{
                    position: 'absolute',
                    top: 0, left: 0,
                    pointerEvents: 'none',
                    zIndex: 0,
                    opacity: isWorking ? 1 : 0,
                    transition: 'opacity 1s ease'
                }}
            />

            <motion.svg
                viewBox="0 0 100 100"
                className="avatar-svg"
                initial={false}
                animate={parallax.head}
                transition={springProps}
                style={{ zIndex: 1 }}
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
                </defs>

                {/* HUD Elements during Hacking */}
                <AnimatePresence>
                    {isWorking && (
                        <motion.g initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }}>
                            <motion.circle
                                cx="50" cy="50" r="48"
                                fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="0.2"
                                strokeDasharray="5,10"
                                animate={{ rotate: 360 }}
                                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                            />
                            <motion.circle
                                cx="50" cy="50" r="40"
                                fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="0.1"
                                strokeDasharray="20,100"
                                animate={{ rotate: -360 }}
                                transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
                            />
                        </motion.g>
                    )}
                </AnimatePresence>

                {/* Character Form */}
                <path
                    d="M50 10 C 20 10 15 40 15 60 C 15 85 35 95 50 95 C 65 95 85 85 85 60 C 85 40 80 10 50 10"
                    fill="url(#soulGradient)"
                    stroke="rgba(255, 255, 255, 0.08)"
                    strokeWidth="0.5"
                />

                {/* Intent/Eyes */}
                <motion.g animate={parallax.eyes} transition={springProps}>
                    <g transform="translate(35, 45)">
                        <circle r="8" fill="rgba(0,0,0,0.8)" />
                        <motion.circle
                            r={isWorking ? 1.5 : 3}
                            fill={isWorking ? "#fff" : "#d4d4d8"}
                            style={{ filter: 'url(#celestial-glow)' }}
                            animate={isWorking ? { opacity: [0.4, 1, 0.4], scale: [1, 1.2, 1] } : {}}
                            transition={{ duration: 0.5, repeat: Infinity }}
                        />
                    </g>
                    <g transform="translate(65, 45)">
                        <circle r="8" fill="rgba(0,0,0,0.8)" />
                        <motion.circle
                            r={isWorking ? 1.5 : 3}
                            fill={isWorking ? "#fff" : "#d4d4d8"}
                            style={{ filter: 'url(#celestial-glow)' }}
                            animate={isWorking ? { opacity: [0.4, 1, 0.4], scale: [1, 1.2, 1] } : {}}
                            transition={{ duration: 0.5, repeat: Infinity, delay: 0.2 }}
                        />
                    </g>
                </motion.g>

                {/* Cognitive Interface */}
                <motion.path
                    d={isWorking ? "M42 75 Q 50 73 58 75" : "M35 75 Q 50 76 65 75"}
                    fill="none"
                    stroke={isWorking ? "#fff" : "rgba(255,255,255,0.2)"}
                    strokeWidth={isWorking ? 1 : 0.5}
                    animate={{ opacity: isWorking ? [0.5, 1, 0.5] : 1 }}
                    transition={{ duration: 1, repeat: Infinity }}
                />

                {/* Hacking Hand / Manipulation */}
                <AnimatePresence>
                    {isWorking && (
                        <motion.g
                            initial={{ y: 20, opacity: 0 }}
                            animate={{ y: 0, opacity: 0.8 }}
                            exit={{ y: 20, opacity: 0 }}
                            transition={springProps}
                        >
                            {/* Floating "Magic" Particles around hands */}
                            {[...Array(3)].map((_, i) => (
                                <motion.circle
                                    key={i}
                                    cx={40 + i * 10} cy="80" r="1.5"
                                    fill="#fff"
                                    style={{ filter: 'url(#celestial-glow)' }}
                                    animate={{
                                        y: [-2, 2, -2],
                                        opacity: [0.2, 0.8, 0.2],
                                        scale: [1, 1.5, 1]
                                    }}
                                    transition={{ duration: 1, repeat: Infinity, delay: i * 0.3 }}
                                />
                            ))}
                        </motion.g>
                    )}
                </AnimatePresence>
            </motion.svg>
        </div>
    );
};

export default Avatar;
