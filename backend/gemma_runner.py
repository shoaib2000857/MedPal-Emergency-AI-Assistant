from transformers import AutoProcessor, AutoModelForImageTextToText
import torch
from typing import List

GEMMA_ID = "google/gemma-3n-E4B-it"

# Load processor and model efficiently
processor = AutoProcessor.from_pretrained(GEMMA_ID)
model = AutoModelForImageTextToText.from_pretrained(
    GEMMA_ID,
    torch_dtype=torch.float16,
    device_map="auto",
    offload_folder="offload",  # Optional but helps on 8 GB GPU
    offload_state_dict=True
)

def move_inputs_to_device(inputs, device, dtype):
    """Ensure all tensors in the input dictionary are on the correct device and dtype."""
    for k in inputs:
        if isinstance(inputs[k], torch.Tensor):
            inputs[k] = inputs[k].to(device=device, dtype=dtype)
    return inputs

def transcribe_and_analyze(audio_path: str) -> str:
    """Transcribe and triage from a single audio file."""
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "audio", "audio": audio_path},
                {"type": "text", "text": "Transcribe this audio and provide a basic medical triage."},
            ]
        }
    ]
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
    )

    inputs = move_inputs_to_device(inputs, model.device, model.dtype)
    outputs = model.generate(**inputs, max_new_tokens=64)
    return processor.batch_decode(outputs, skip_special_tokens=True)[0]

def run_audio_query(audio_urls: List[str], instruction: str, max_tokens: int = 64) -> str:
    """Process multiple audio files using a common instruction."""
    messages = [{
        "role": "user",
        "content": [{"type": "audio", "audio": url} for url in audio_urls] +
                   [{"type": "text", "text": instruction}]
    }]
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
    )

    inputs = move_inputs_to_device(inputs, model.device, model.dtype)
    outputs = model.generate(**inputs, max_new_tokens=max_tokens)
    return processor.batch_decode(outputs, skip_special_tokens=True)[0]
