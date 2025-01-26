import { useParams } from "react-router";
import React, { useState, useEffect } from "react";

export default function ReportPage() {
  const { userId, postId } = useParams();
  const [reportData, setReportData] = useState(null);
  const [error, setError] = useState("");

  const breathingTips = [
    "1. Deep Belly Breathing: Place one hand on your belly and the other on your chest. Breathe in deeply through your nose for 4 seconds, letting your belly rise. Exhale slowly through your mouth for 6 seconds. Repeat for 2-3 minutes.",
    "2. Box Breathing: Inhale through your nose for 4 seconds, hold your breath for 4 seconds, exhale through your mouth for 4 seconds, and pause for 4 seconds before repeating.",
    "3. 4-7-8 Technique: Inhale through your nose for 4 seconds, hold your breath for 7 seconds, and exhale through your mouth for 8 seconds. Repeat this cycle 4-5 times.",
    "4. Progressive Relaxation: While inhaling deeply, tense one muscle group (e.g., your feet) for 5 seconds, then exhale and release. Move up the body, focusing on different muscle groups.",
    "5. Mindful Meditation: Find a quiet place, close your eyes, and focus on your breath. If your mind wanders, gently bring your attention back to your breathing.",
    "6. Gratitude Breathing: While taking deep breaths, think of three things you’re grateful for, one for each inhale.",
  ];

  useEffect(() => {
    const fetchReport = async () => {
        try {
            const token = localStorage.getItem("token");
            if (!token) {
                setError("You must be logged in to view this report.");
                return;
            }

            const response = await fetch(`http://localhost:8000/hrdata/data/${userId}/${postId}`, {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Failed to fetch report.");
            }

            const data = await response.json();
            setReportData(data);
        } catch (error) {
            console.error("Error fetching report:", error);
            setError(error.message);
        }
    };

    fetchReport();
  }, [userId, postId]);

  if (error) {
    return <p>Error: {error}</p>;
  }

  if (!reportData) {
    return <p>Loading...</p>;
  }

  return (
    <div className="p-4 bg-gradient-to-r from-purple-50 to-violet-200 h-full lg:h-screen">
        <div className="mt-24 flex flex-col items-center">
            <h1 className="text-2xl sm:text-3xl font-bold flex justify-center items-center">Generated Report Details</h1>
            <div className="mt-4 p-0.5 sm:p-4 flex justify-center space-x-4 items-center bg-slate-50 border rounded-xl border-violet-400">
                <div className="text-right text-xl">
                    <h3><strong>BPM: </strong></h3>
                    <h3><strong>SDNN: </strong></h3>
                    <h3><strong>RMSSD: </strong></h3>
                    <h3><strong>pNN50: </strong></h3>
                    <h3><strong>Stress Indicator: </strong></h3>
                </div>
                <div className="text-left text-xl">
                    <h3>{reportData.BPM}</h3>
                    <h3>{reportData.SDNN}</h3>
                    <h3>{reportData.RMSSD}</h3>
                    <h3>{reportData.pNN50}</h3>
                    <h3>{reportData.stress_indicator}</h3>
                </div>
            </div>
            <h1 className="mt-12 text-2xl sm:text-3xl font-bold flex justify-center items-center">Helpful Stress Relieving Tips</h1>
            <div className="mt-4 p-0.5 sm:p-4 flex flex-col justify-center text-left bg-slate-50 border rounded-xl border-violet-400 w-9/12 max-w-[1075px]">
                {breathingTips.map((tip, index) => (
                    <p key={index} className="m-2 text-base sm:text-lg text-slate-800" dangerouslySetInnerHTML={{ __html: tip }}></p>
                ))}
            </div>
        </div>
    </div>
  );
}
