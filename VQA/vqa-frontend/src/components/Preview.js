import React from "react";

function Preview({ file }) {
  if (!file) {
    return null; // No file selected, show nothing
  }

  const imageUrl = URL.createObjectURL(file);

  return (
    <div className="mt-6 ml-12">
      <h3 className="text-lg font-semibold mb-2">Image Preview:</h3>
      <img
        src={imageUrl}
        alt="Uploaded Preview"
        className="w-80 rounded shadow"
      />
    </div>
  );
}

export default Preview;
