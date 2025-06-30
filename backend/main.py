from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.gemma_runner import transcribe_and_analyze
from backend.audio_tools import convert_webm_to_wav, preprocess_audio
import shutil
import uuid
import os

app = FastAPI()

# CORS configuration (allow Tauri frontend to access backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Lock this down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-audio/")
async def analyze_audio(file: UploadFile = File(...)):
    temp_ext = os.path.splitext(file.filename)[1] or ".webm"
    temp_input = f"temp_{uuid.uuid4().hex}{temp_ext}"
    with open(temp_input, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Convert if needed
    if temp_input.endswith(".webm"):
        wav_file = convert_webm_to_wav(temp_input)
        os.remove(temp_input)
    else:
        wav_file = temp_input

    # Preprocess
    processed_file = preprocess_audio(wav_file)
    os.remove(wav_file)

    try:
        result = transcribe_and_analyze(processed_file)
        return {"result": result}
    finally:
        os.remove(processed_file)
