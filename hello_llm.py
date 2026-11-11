import requests
import os

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"
TIMEOUT = float(os.getenv("LLM_TIMEOUT", "60"))

class LLMUnavailableError(Exception):
    pass

class LLMTimeOutError(Exception):
    pass

class LLMUpstreamError(Exception):
    pass

def ask(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = {
        "reply": "",
        "prompt_tokens": 0,
        "completion_tokens": 0
    }
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
        if r.status_code != requests.codes.ok:
            raise LLMUpstreamError(f"Ollama returned {r.status_code}: {r.text[:200]}")
        else:
            response["reply"] = r.json()["response"]
            response["prompt_tokens"] = r.json()["prompt_eval_count"]
            response["completion_tokens"] = r.json()["eval_count"]
            return response
        
    except requests.exceptions.ConnectionError as e:
        raise LLMUnavailableError(f"Can't reach Ollama at {OLLAMA_URL}: {e}")

    except requests.exceptions.Timeout as e:
        raise LLMTimeOutError(f"Time out {TIMEOUT}")
        

if __name__ == "__main__":
    print(ask("Explain what an LLM gateway is in one sentence."))