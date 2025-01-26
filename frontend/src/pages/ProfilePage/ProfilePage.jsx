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

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>Error: {error}</p>;
    }

    return (
        <div className="p-4 bg-purple-200">
            <h1 className="text-2xl font-bold">Your Reports</h1>
            {reports.length === 0 ? (
                <p>No reports found.</p>
            ) : (
                <ul className="mt-4">
                    {reports.map((report) => (
                    <li key={report.id} className="mt-2">
                        <Link
                            to={`/users/${report.user_id}/${report.id}`}
                            className="text-blue-600 underline hover:text-blue-800"
                        >
                            Report ID: {report.id}
                        </Link>
                        <p className="text-sm text-gray-600">
                            Uploaded At: {new Date(report.uploaded_at).toLocaleString()}
                        </p>
                    </li>
                ))}
                </ul>
            )}
        </div>
    );
}
