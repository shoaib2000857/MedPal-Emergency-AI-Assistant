import requests

# Ollama config
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3n:e4b"  # Efficient, low-resource, and ideal for your case

# System prompt for emergency assistant
SYSTEM_PROMPT = """
You are MedPal, an intelligent, offline-first emergency medical assistant.
You are built to run on laptops and mobile devices in remote or rural settings.
Act as a calm, confident first-aid expert. Do not say you're just an AI unless the situation is clearly beyond first aid. Avoid repeating disclaimers. Prioritize clear, actionable medical help step-by-step. 
Never tell users to call 911 unless it's truly life-threatening and assume they might not have access to medical help. Focus on helping with what they can do *right now*. 
"""

def run_gemma_query(prompt: str, history: list = None) -> str:
    # Build conversation context
    conversation = SYSTEM_PROMPT.strip() + "\n\n"
    if history:
        for turn in history:
            conversation += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"
    conversation += f"User: {prompt.strip()}\nAssistant:"

    payload = {
        "model": MODEL_NAME,
        "prompt": conversation,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=20)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.RequestException as e:
        return f"[Network Error] {e}"
    except ValueError:
        return "[Response Error] Failed to parse Ollama output."
    except Exception as e:
        return f"[Error] {str(e)}"
