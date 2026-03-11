"use client"

import {colors} from "@/app/lib/tokens";
import {useEffect, useState } from "react";

interface MyceliumBackgroundProps {
    opacity?: number         // overall opacity, default 0.18
    color?: string           // thread color, default #7a9e7e
    nodeColor?: string       // node color, default #a8c5a0
    density?: "low" //| "medium" | "high"  // how many threads
    animated?: boolean       // pulse animation, default true
    drawIn?: boolean         // draw-in animation on load, default true
    fixed?: boolean          // fixed or absolute positioning, default true
    className?: string
}

// Thread data — path, dasharray length, animation duration, delay
function buildThreads(width: number, height: number, density: string) {
    switch (density) {

        default: //Low
            return  [
                { d: `M0,400 Q150,188 290,350 T600,300 T875,250 T1200,320`, len: width, dur: 8, delay: 0 },
                { d: "M850,0 Q800,350 515,525 T0,500", len: width, dur: 11, delay: 1 },
                { d: "M1000,0 Q1150,350 880,800 T850,1100", len: width, dur: 7, delay: 3 },
                { d: "M200,0 Q200,450 400,520 T700,480 T1000,580 T1200,500", len: width, dur: 5, delay: 1 },
                { d: "M700,0 Q350,150 480,400 T450,700 T500,800", len: height, dur: 9, delay: 2 },
            ]
    }

}

// Hook
function useWindowSize() {
 // Initialize state with undefined width/height so server and client renders match
  const [windowSize, setWindowSize] = useState({
    width: 1200,
    height: 800,
  });
  useEffect(() => {
    // only execute all the code below in client side
    // Handler to call on window resize
    function handleResize() {
      // Set window width/height to state
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    // Add event listener
    window.addEventListener("resize", handleResize);

    // Call handler right away so state gets updated with initial window size
    handleResize();

    // Remove event listener on cleanup
    return () => window.removeEventListener("resize", handleResize);
  }, []); // Empty array ensures that effect is only run on mount
  return windowSize;
}


const BRANCHES = [
    {d:"M232,300 Q150 350 150,  500", len: 900 , dur:9, delay:0.5},
    {d:"M700,480 Q550,870 7200, 500", len: 300 , dur:6, delay:0.5},
    {d:"M580,323 Q800,200 1000, 475", len: 900 , dur:8, delay:0.5},
]

const NODES = [
    //Low left -med/high
    //  { cx: 200, cy: 600, r: 2, glowR: 6, dur: 5, delay: 0.8 },
    //  //low right - med/high
    //  { cx: 990, cy: 570, r: 2.5, glowR: 8, dur: 3.5, delay: 1.5 },
    //  //high right - med/high
    //  { cx: 920, cy: 303, r: 2, glowR: 6, dur: 4, delay: 1.8 },

    { cx: 232, cy: 300, r: 2, glowR: 5, dur: 6, delay: 2 },
    { cx: 482, cy: 404, r: 2, glowR: 7, dur: 4, delay: 1 },
    { cx: 580, cy: 323, r: 2, glowR: 6, dur: 5, delay: 2.5 },
    { cx: 700, cy: 480, r: 2, glowR: 7, dur: 4.5, delay: 0.3 },
]


export default function MyceliumBackground({
                                               opacity = 0.18,
                                               color = colors.mycopsiPurple_200,
                                               nodeColor = colors.mycopsiYellow_100,
                                               density = "low",
                                               animated = true,
                                               drawIn = true,
                                               fixed = true,
                                               className = ""
                                           }: MyceliumBackgroundProps) {
    const size = useWindowSize();

    const threads = buildThreads(size.width, size.height, density)
    const position = fixed ? "fixed" : "absolute"



    return (
        <div className={`mycelium-root ${className} pointer-events-none inset-0 z-0`}
             aria-hidden="true"
             style={{position}}>
            <svg viewBox="0 0 1200 800"
                 preserveAspectRatio="xMidYMid slice"
                 className="w-full h-full"
                 style={{opacity}}>
                <defs>
                    {NODES.map((node, i) => (
                        <radialGradient key={i} id={`glow-${i}`} cx="50%" cy="50%" r="50%">
                            <stop offset="0%" stopColor={nodeColor} stopOpacity="0.4"/>
                            <stop offset="100%" stopColor={nodeColor} stopOpacity="0"/>
                        </radialGradient>
                    ))}
                </defs>

                {/* Main threads */}
                {threads.map((t, i) => (
                    <path
                        key={i}
                        d={t.d}
                        fill="none"
                        stroke={color}
                        strokeWidth="0.8"
                        strokeLinecap="round"
                        style={{
                            strokeDasharray: t.len,
                            strokeDashoffset: drawIn ? t.len : 0,
                            animation: [
                                drawIn ? `mycelium-draw ${t.dur * 0.4}s ease ${t.delay}s forwards` : "",
                                animated ? `mycelium-pulse ${t.dur}s ease-in-out ${t.delay}s infinite` : "",
                            ].filter(Boolean).join(", ") || "none",
                        }}
                    />
                ))}

                {/* Branches */}
                {BRANCHES.map((b, i) => (
                    <path
                        key={i}
                        d={b.d}
                        fill="none"
                        stroke={color}
                        strokeWidth="0.5"
                        strokeLinecap="round"
                        style={{
                            opacity: 0.7,
                            strokeDasharray: b.len,
                            strokeDashoffset: drawIn ? b.len : 0,
                            animation: [
                                drawIn ? `mycelium-draw ${b.dur * 0.3}s ease ${b.delay + 1}s forwards` : "",
                                animated ? `mycelium-pulse ${b.dur}s ease-in-out ${b.delay}s infinite` : "",
                            ].filter(Boolean).join(", ") || "none",
                        }}
                    />
                ))}

                {/* Nodes */}
                {NODES.map((node, i) => (
                    <g key={i}>
                        {/* glow halo */}
                        <circle
                            cx={node.cx}
                            cy={node.cy}
                            r={node.glowR}
                            fill={`url(#glow-${i})`}
                            style={{
                                animation: animated
                                    ? `mycelium-glow ${node.dur}s ease-in-out ${node.delay}s infinite`
                                    : "none",
                            }}
                        />
                        {/* solid dot */}
                        <circle
                            cx={node.cx}
                            cy={node.cy}
                            r={node.r}
                            fill={nodeColor}
                            opacity={0.9}
                        />
                    </g>
                ))}
            </svg>
        </div>

    )
}
