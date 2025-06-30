# audio_handler.py
import whisper
import os

# Load model once on import (CPU only)
model = whisper.load_model("base").to("cpu")

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes the given audio file using Whisper on CPU.
    """
    try:
        print(f"[INFO] Transcribing {file_path} on CPU...")
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        print(f"[ERROR] Transcription failed: {e}")
        return "Transcription failed due to an error."
