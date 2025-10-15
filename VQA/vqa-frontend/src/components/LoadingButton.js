import React from "react";
import "../App.css"; // for the loader CSS

function LoadingButton({ loading }) {
  return (
    <button
      type="submit"
      disabled={loading}
      className="bg-primary text-white px-6 py-3 mb-4 rounded-lg hover:bg-accent transition duration-300 disabled:opacity-50"
    >
    
      {loading ? (
        <div className="bg-primary text-white px-6 py-2 rounded hover:bg-accent transition disabled:opacity-50"></div>
      ) : (
        "Ask"
      )}
    </button>

  );
}

export default LoadingButton;
