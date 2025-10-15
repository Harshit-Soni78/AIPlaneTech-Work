import React from "react";

function FileUpload({ onFileChange }) {
  return (
    <div className="mb-4 ml-10 p-6">
      <input
        type="file"
        onChange={(e) => {
          onFileChange(e.target.files[0]);
        }}
        required
        className="border border-gray-700 bg-gray-900 text-white rounded px-4 py-2"
      />
    </div>
  );
}

export default FileUpload;
