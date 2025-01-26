import React from "react";
import { motion } from "framer-motion";

const EkgSvg = () => {
  return (
    <svg viewBox="0 0 500 100" width="100%" height="100" style={{ background: "tra" }}>
      <motion.polyline
        points="100,50 150,50 170,20 190,80 210,50 260, 50 280, 10 300, 90 320, 50 400, 50 "
        
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
