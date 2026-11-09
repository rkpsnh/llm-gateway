import requests
import os

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"
TIMEOUT = float(os.getenv(""))

class LLMUnavailableError(Exception):
    pass

def ask(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        if r.status_code != requests.codes.ok:
            raise Exception("Status code is not 2xx")
        else:
            return r.json()["response"]
        
    except requests.exceptions.ConnectionError as e:
        raise LLMUnavailableError(f"Can't reach Ollama at {OLLAMA_URL}: {e}")
        

if __name__ == "__main__":
    print(ask("Explain what an LLM gateway is in one sentence."))