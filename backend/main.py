from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.audio_tools import transcribe_audio
from backend.gemma_runner import run_gemma_query

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str
    history: list = []

@app.post("/analyze-text/")
async def analyze_text(req: TextRequest):
    response = run_gemma_query(req.text, req.history)
    return {"response": response}

@app.post("/analyze-audio/")
async def analyze_audio(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    transcript = transcribe_audio(temp_path)
    response = run_gemma_query(transcript)
    return {"transcription": transcript, "response": response}
