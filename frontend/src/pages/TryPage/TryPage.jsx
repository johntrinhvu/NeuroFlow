import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function TryPage() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [error, setError] = useState("");
    const navigate = useNavigate();
    
    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
        setError("");
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!selectedFile) {
            setError("Please select a file before submitting.");
            return;
        }

        const token = localStorage.getItem("token");
        if (!token) {
            setError("You must be logged in to upload a file.");
            return;
        }

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            const response = await fetch("http://localhost:8000/hrdata/video/upload", {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Failed to process the video.");
            }

            const data = await response.json();
            console.log("Upload successful:", data);

            // Assuming the backend returns userId and postId
            const userId = "your_user_id_logic"; // Replace with actual logic to get userId
            const postId = data.report_id; // Replace with actual response from backend

            navigate(`/users/${userId}/${postId}`);
        } catch (error) {
            console.error("Upload error:", error);
            setError(error.message);
        }
    };

    return (
        <div className="flex flex-col lg:flex-row items-center lg:justify-center bg-gradient-to-r from-purple-50 to-violet-200 lg:h-screen">
            <div className="mt-32 flex flex-col items-center">
                <div className="flex flex-col items-center w-6/12">
                    <div className="flex items-center justify-center">
                        <div className="flex items-center justify-center w-16 h-16 rounded-full bg-purple-900 text-white text-3xl font-bold">1</div>
                    </div>
                    <h1 className="font-semibold text-2xl mt-4">A Simple, Easy Process</h1>
                    <p className="flex items-center justify-center mt-2">Getting started is quick and straightforward. Follow these steps, and you'll be on your way to generating your report in no time.</p>
                </div>

                <div className="mt-6 flex flex-col items-center w-8/12">
                    <div className="flex items-center justify-center">
                        <div className="flex items-center justify-center w-16 h-16 rounded-full bg-purple-900 text-white text-3xl font-bold">2</div>
                    </div>
                    <h1 className="font-semibold text-2xl mt-4">Upload Your Video</h1>
                    <ul>
                        <li className="mt-2">
                            <p>
                                • Select your video file by clicking the "Choose File" Button.
                            </p>
                        </li>
                        <li className="mt-2">
                            <p>
                                • Make sure your video is in the correct format (e.q., MP4, MOV).
                            </p>
                        </li>
                        <li className="mt-2">
                            <p>
                                • Hit "Generate Report" to start processing.
                            </p>
                        </li>
                    </ul>
                </div>

                <div className="mt-10 flex flex-col items-center w-8/12">
                    <div className="flex items-center justify-center">
                        <div className="flex items-center justify-center w-16 h-16 rounded-full bg-purple-900 text-white text-3xl font-bold">3</div>
                    </div>
                    <h1 className="font-semibold text-2xl mt-4">Generate Your Report</h1>
                    <ol>
                        <li className="mt-2">
                            <h5 className="font-semibold">1. Wait for Processing.</h5>
                            <p>The system will analyze your video.</p>
                        </li>
                        <li className="mt-2">
                            <h5 className="font-semibold">2. Preview Results.</h5>
                            <p>You'll see a summary of key findings.</p>
                        </li>
                        <li className="mt-2">
                            <h5 className="font-semibold">3. Download the Report.</h5>
                            <p>Click "Download Report" to download your detailed insights.</p>
                        </li>
                    </ol>
                </div>

            </div>
            <div className="lg:mr-52 mt-6 p-2 bg-purple-50 border-violet-500 border m-4 rounded-xl">
                <form onSubmit={handleSubmit} className="flex flex-col items-center justify-center gap-10" encType="multipart/form-data">
                    <input className="flex items-center justify-center" type="file" name="file" onChange={handleFileChange} />
                    <button type="submit" className="p-2 transition ease-in-out hover:bg-purple-900 bg-purple-800 border-2 border-violet-700 text-white rounded-xl">Generate Report</button>
                </form>
            </div>
        </div>
    );
}