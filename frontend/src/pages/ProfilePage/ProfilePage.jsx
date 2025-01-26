import { useParams } from "react-router";
import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import { UserContext } from "../../contexts/UserContext/UserContext";

export default function ProfilePage() {
    const { userId } = useParams();
    const { user } = useContext(UserContext);
    const [reports, setReports] = useState([]);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchReports = async () => {
            try {
                const token = localStorage.getItem("token");
                if (!token) {
                    setError("You must be logged in to view this page.");
                    return;
                }

                const response = await fetch(`http://localhost:8000/hrdata/data/${userId}`, {
                    method: "GET",
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || "Failed to fetch reports.");
                }

                const data = await response.json();
                const sortedReports = data.hr_data.sort((a, b) => new Date(b.uploaded_at) - new Date(a.uploaded_at));
                setReports(sortedReports);
            } catch (err) {
                console.error("Error fetching reports:", err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchReports();
    }, [userId]);

    const handleDownloadPDF = async () => {
        try {
            const token = localStorage.getItem("token");
            if (!token) {
                setError("You must be logged in to download the report.");
                return;
            }

            const response = await fetch(`http://localhost:8000/hrdata/download`, {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Failed to download the report.");
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "stress_report.pdf";
            a.click();
            window.URL.revokeObjectURL(url);
        } catch (err) {
            console.error("Error downloading report:", err);
            setError(err.message);
        }
    };

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>Error: {error}</p>;
    }

    return (
        <div className="p-4 bg-gradient-to-r from-purple-50 to-violet-200 h-screen">
            <div className="mt-24 flex flex-col items-center">
                <h1 className="text-2xl font-bold">Your Reports</h1>
                {reports.length === 0 ? (
                    <p>No reports found.</p>
                ) : (
                    <div className="mt-4 w-9/12 max-w-[1070px]">
                        <div className="flex justify-center">
                            <button onClick={handleDownloadPDF} className="transition ease-in-out hover:bg-violet-900 bg-violet-800 text-white px-4 py-2 rounded-xl">Download PDF Version of Report</button>
                        </div>
                        <div className="mt-4">
                            <ul>
                                {reports.map((report) => (
                                <Link
                                    to={`/users/${report.user_id}/${report.id}`}
                                >
                                    <li key={report.id} className="transition ease-in-out hover:bg-slate-200 mt-2 border border-violet-400 bg-slate-50 rounded-xl p-4 flex flex-col">
                                        <div className="flex space-x-2">
                                            <h1 className="font-semibold">Report ID: </h1>
                                            <p>{report.id.slice(0, 10)}{report.id.length > 10 ? '...' : ''}</p>
                                        </div>
                                        <p className="text-sm text-gray-600">
                                            Uploaded At: {new Date(report.uploaded_at).toLocaleString("en-US", { timeZone: "America/Los_Angeles" })}
                                        </p>
                                    </li>
                                </Link>
                                
                            ))}
                            </ul>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
