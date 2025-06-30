import librosa
import soundfile as sf
import numpy as np
import uuid
import os
import subprocess

def convert_webm_to_wav(input_file: str) -> str:
    """Converts a .webm audio file to temporary .wav using ffmpeg."""
    temp_wav = f"temp_{uuid.uuid4().hex}.wav"
    cmd = [
        "ffmpeg", "-y",
        "-i", input_file,
        "-ac", "1",        # mono
        "-ar", "16000",    # 16kHz sample rate
        "-f", "wav",
        temp_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return temp_wav

def preprocess_audio(input_file: str, target_sr=16000) -> str:
    """Converts, resamples, normalizes, and outputs audio to a clean WAV format."""
    # Convert webm if needed
    file_ext = os.path.splitext(input_file)[-1].lower()
    if file_ext == ".webm":
        input_file = convert_webm_to_wav(input_file)

    # Load and normalize
    audio, sr = librosa.load(input_file, sr=target_sr, mono=True)
    audio = np.clip(audio, -1.0, 1.0).astype(np.float32)

    output_file = f"processed_{uuid.uuid4().hex}.wav"
    sf.write(output_file, audio, target_sr)
    return output_file
