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
    <div className="p-4 bg-gradient-to-r from-purple-50 to-violet-200 h-screen">
        <div className="mt-24 flex flex-col">
            <h1 className="text-2xl sm:text-3xl font-bold flex justify-center">Generated Report Details</h1>
            <div className="mt-4 flex justify-center space-x-8 items-center ">
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
        </div>
    </div>
  );
}
