"use client";

import { motion } from "framer-motion";

export function AppBackground() {
  return (
    <div className="pointer-events-none fixed inset-0 overflow-hidden">
      <motion.div
        animate={{
          x: [0, 80, 0],
          y: [0, 40, 0],
        }}
        transition={{
          duration: 18,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute -left-40 -top-40 h-[520px] w-[520px] rounded-full bg-cyan-500/15 blur-[140px]"
      />

      <motion.div
        animate={{
          x: [0, -60, 0],
          y: [0, -60, 0],
        }}
        transition={{
          duration: 22,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute bottom-0 right-0 h-[520px] w-[520px] rounded-full bg-violet-500/15 blur-[150px]"
      />

      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.04),transparent_60%)]" />

      <div className="absolute inset-0 bg-[#050816]" />
    </div>
  );
}