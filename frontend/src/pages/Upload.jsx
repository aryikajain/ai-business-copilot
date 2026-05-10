import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { UploadCloud, FileSpreadsheet } from "lucide-react";

import Navbar from "../components/Navbar";
import API from "../api";

export default function Upload() {
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    const token = localStorage.getItem("token");

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const response = await API.post("/upload", formData, {
        params: { token },
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      localStorage.setItem(
        "analysis",
        JSON.stringify(response.data.analysis)
      );

      navigate("/dashboard");
    } catch (error) {
      alert(error.response?.data?.detail || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-slate-50 flex items-center justify-center px-6">

        <div className="w-full max-w-2xl bg-white rounded-3xl shadow-xl p-10">

          {/* Heading */}
          <div className="text-center mb-10">
            <div className="w-20 h-20 bg-blue-100 rounded-3xl flex items-center justify-center mx-auto mb-5">
              <UploadCloud size={40} className="text-blue-600" />
            </div>

            <h1 className="text-4xl font-bold text-gray-900 mb-3">
              Upload Business Data
            </h1>

            <p className="text-gray-500 text-lg">
              Upload your CSV file and let AI generate business insights,
              customer segmentation, and growth recommendations.
            </p>
          </div>

          {/* Upload Box */}
          <div className="border-2 border-dashed border-gray-300 rounded-3xl p-10 text-center bg-slate-50">

            <input
              type="file"
              accept=".csv"
              onChange={(e) => setFile(e.target.files[0])}
              className="mb-6"
            />

            {!file ? (
              <>
                <FileSpreadsheet
                  size={48}
                  className="mx-auto text-gray-400 mb-4"
                />

                <p className="text-gray-600">
                  Select a CSV file to begin analysis
                </p>
              </>
            ) : (
              <>
                <FileSpreadsheet
                  size={48}
                  className="mx-auto text-green-500 mb-4"
                />

                <p className="text-lg font-semibold text-gray-800">
                  {file.name}
                </p>

                <p className="text-sm text-gray-500 mt-2">
                  Ready for AI analysis
                </p>
              </>
            )}
          </div>

          {/* Button */}
          <button
            onClick={handleUpload}
            disabled={loading}
            className="w-full mt-8 bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-2xl font-semibold text-lg transition-all duration-200"
          >
            {loading ? "Analyzing Business Data..." : "Upload & Analyze"}
          </button>
        </div>
      </div>
    </>
  );
}