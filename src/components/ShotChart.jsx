import React, { useMemo } from 'react';

const ShotChart = ({ shots }) => {
    // NBA court coordinates are roughly -250 to 250 (width) and -50 to 450 (height)
    // We normalize these to a viewbox

    const points = useMemo(() => {
        if (!shots) return [];
        return shots.map((shot, i) => ({
            x: shot.LOC_X,
            y: shot.LOC_Y,
            made: shot.SHOT_MADE_FLAG === 1,
            type: shot.SHOT_TYPE
        }));
    }, [shots]);

    return (
        <div className="w-full aspect-[50/47] glass-card p-6 overflow-hidden relative">
            <h3 className="text-xl font-bold mb-4 opacity-60">SHOT CHART</h3>
            <div className="relative w-full h-full bg-black/20 rounded-lg overflow-hidden border border-white/5">
                <svg viewBox="-250 -50 500 470" className="w-full h-full">
                    {/* Court markings */}
                    <g fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="2">
                        {/* Backboard */}
                        <line x1="-30" y1="-7" x2="30" y2="-7" />
                        {/* Outer Box */}
                        <rect x="-80" y="-47" width="160" height="190" />
                        {/* Inner Box */}
                        <rect x="-60" y="-47" width="120" height="190" />
                        {/* Rim */}
                        <circle cx="0" cy="0" r="7.5" />
                        {/* Restricted Area */}
                        <path d="M-40 0 a40 40 0 1 1 80 0" />
                        {/* Three Point Line */}
                        <path d="M-220 -47 L-220 90 a220 220 0 0 1 440 0 L 440 -47" />
                        {/* Key Circle */}
                        <circle cx="0" cy="143" r="60" />
                    </g>

                    {/* Shots */}
                    {points.map((p, i) => (
                        <circle
                            key={i}
                            cx={p.x}
                            cy={p.y}
                            r="4"
                            className={`transition-all duration-300 hover:r-6 ${p.made ? 'fill-green-400 opacity-80 shadow-[0_0_8px_rgba(74,222,128,0.5)]' : 'fill-red-500 opacity-40'
                                }`}
                        >
                            <title>{p.made ? 'Made' : 'Missed'}</title>
                        </circle>
                    ))}
                </svg>
            </div>

            <div className="flex gap-4 mt-4 justify-center">
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-green-400"></div>
                    <span className="text-xs text-white/60">MADE</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-red-500"></div>
                    <span className="text-xs text-white/60">MISSED</span>
                </div>
            </div>
        </div>
    );
};

export default ShotChart;
