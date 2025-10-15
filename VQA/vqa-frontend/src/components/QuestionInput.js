import React from "react";

function QuestionInput({ question, onQuestionChange }) {
  return (
    <div className="mb-4 ml-10">
      <input
        type="text"
        placeholder="Enter your question"
        value={question}
        onChange={(e) => onQuestionChange(e.target.value)}
        required
        className="w-[400px] border border-gray-700 bg-white text-black rounded px-4 py-2 shadow"
      />
      
    </div>
  );
}

export default QuestionInput;
