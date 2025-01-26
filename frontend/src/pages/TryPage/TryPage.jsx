import React, { useState } from "react";

export default function TryPage() {
    const [selectedFile, setSelectedFile] = useState(null);
    
    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
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
            <div className="lg:mr-52 mt-6 p-2 bg-slate-200 border-slate-300 border-2 m-4 rounded-xl">
                <form className="flex flex-col items-center justify-center gap-10" encType="multipart/form-data">
                    <input className="flex items-center justify-center" type="file" name="file" onChange={handleFileChange} />
                    <button type="submit" className="p-2 transition ease-in-out hover:bg-purple-900 bg-purple-800 border-2 border-violet-700 text-white rounded-xl">Generate Report</button>
                </form>
            </div>
        </div>
    );
}