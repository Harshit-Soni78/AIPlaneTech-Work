import React from "react";
import ReactMarkdown from "react-markdown";

function AnswerDisplay({ answer }) {
  if (!answer) return null;

  return (
    <div className="mt-5 ml-10 text-left leading-relaxed tracking-wide">
      <h3 className="text-xl font-semibold mb-2">Answer:</h3>
      <div className="prose prose-invert">
      <ReactMarkdown>{answer}</ReactMarkdown>
      </div>
    </div>
  );
}

export default AnswerDisplay;
// This component displays the answer in a markdown format.
// It uses the `react-markdown` library to render the answer text.