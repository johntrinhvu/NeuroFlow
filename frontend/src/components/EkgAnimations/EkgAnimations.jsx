import React from "react";
import { motion } from "framer-motion";

const EkgSvg = () => {
  return (
    <svg viewBox="0 0 500 100" width="100%" height="100" style={{ background: "tra" }}>
      <motion.polyline
        points="0,50 50,50 70,20 90,80 110,50 160, 50 180, 20 200, 80 220, 50 300, 50 "

        fill="none"
        stroke="white"
        strokeWidth="3"
        initial={{ strokeDasharray: 1000, strokeDashoffset: 1000, strokeOpacity: 1 }}
        animate={{ strokeDashoffset: 0, strokeOpacity: 0 }} // Add fading animation
        transition={{ duration: 2, ease: "linear", repeat: Infinity }}
      />
    </svg>
  );
};

export default EkgSvg;
