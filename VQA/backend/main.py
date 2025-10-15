import os
import base64
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# FastAPI app
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"message": "Visual QnA API is running. Visit /docs for Swagger UI."}

@app.post("/vqa")
async def visual_qna(file: UploadFile = File(...), question: str = Form(...)):
    try:
        image_bytes = await file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        image_data_url = f"data:{file.content_type};base64,{image_base64}"
   

        # Call Gemini API with image + question
        response = model.generate_content(
            [
                {"mime_type": file.content_type, "data": image_bytes},
                question
            ]
        )

        return JSONResponse(content={
            "question": question,
            "answer": response.text,
            "image_data_url": image_data_url        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Uvicorn server start
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
