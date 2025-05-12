import React, { useState } from "react";
import { useTheme } from "@/hooks/useTheme";

const UploadModelOverlay = ({ onClose, onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const { theme } = useTheme();
  const isDark = theme === "dark";

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/api/models/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (res.ok) {
        alert("Model uploaded successfully!");
        onUploadSuccess(); // Refresh models list
        onClose();
      } else {
        alert(`Error: ${data.detail}`);
      }
    } catch (err) {
      alert("Upload failed.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center px-4">
      <div className={`w-full max-w-md p-6 rounded-2xl shadow-xl ${isDark ? "bg-gray-900 text-white" : "bg-white text-gray-900"}`}>
        <h2 className="text-xl font-semibold mb-4 text-center">Upload New Trading Model</h2>

        <input
          type="file"
          accept=".joblib"
          onChange={(e) => setFile(e.target.files[0])}
          className="w-full mb-4 text-sm"
        />

        <div className="flex justify-end gap-2">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded bg-gray-300 dark:bg-gray-700 text-black dark:text-white"
          >
            Cancel
          </button>
          <button
            onClick={handleUpload}
            disabled={!file || uploading}
            className={`px-4 py-2 rounded text-white ${uploading ? "bg-gray-500" : "bg-blue-600 hover:bg-blue-500"}`}
          >
            {uploading ? "Uploading..." : "Upload"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default UploadModelOverlay;
