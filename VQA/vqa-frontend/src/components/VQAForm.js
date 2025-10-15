import React, { useState } from "react";
import axios from "axios";
import FileUpload from "./FileUpload";
import QuestionInput from "./QuestionInput";
import LoadingButton from "./LoadingButton";
import AnswerDisplay from "./AnswerDisplay";
import Preview from "./Preview";
import Header from "./Header";

function VQAForm() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("question", question);

    try {
      const response = await axios.post("http://localhost:8000/vqa", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setAnswer(response.data.answer);
    } catch (error) {
      console.error("Error sending request:", error);
      alert("There was an error processing your request.");
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (selectedFile) => {
    setFile(selectedFile);
    setAnswer("");
  };

  const handleQuestionChange = (value) => {
    setQuestion(value);
  };

  return (
    <div>
      <>
        <Header />
        <div className="p-6">       
        </div>
      </>

      <form onSubmit={handleSubmit}className="flex items-center gap-4 mb-6 px-12">
        <FileUpload onFileChange={handleFileChange} />
        <div className="flex items-center gap-4">
          <QuestionInput question={question} onQuestionChange={handleQuestionChange} />
          <LoadingButton loading={loading} />
        </div>

      </form>
      <div className="flex items-start gap-8 px-12">
        <Preview file={file} />
        <AnswerDisplay answer={answer} />
      </div>

    </div>
  );
}

export default VQAForm;
