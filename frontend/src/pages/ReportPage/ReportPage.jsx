import { useParams } from "react-router";
import React, { useState, useEffect } from "react";

export default function ReportPage() {
  const { userId, postId } = useParams();
  const [reportData, setReportData] = useState(null);
  const [error, setError] = useState("");

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
    <div className="mt-24 p-4 bg-purple-200">
        <div>
            <h1 className="text-2xl font-bold">Your Generated Report Details</h1>
            <h2 className="text-xl font-bold">Stats</h2>
            <p><strong>BPM:</strong> {reportData.BPM}</p>
                <p><strong>SDNN:</strong> {reportData.SDNN}</p>
                <p><strong>RMSSD:</strong> {reportData.RMSSD}</p>
                <p><strong>pNN50:</strong> {reportData.pNN50}</p>
                <p><strong>Stress Indicator:</strong> {reportData.stress_indicator}</p>
        </div>
    </div>
  );
}
