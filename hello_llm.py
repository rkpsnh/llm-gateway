import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"

def ask(prompt):
    payload = {
        # TODO: add "model", "prompt", and "stream": False
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        # TODO: POST payload as JSON to OLLAMA_URL (add a timeout!)
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        # TODO: raise an error if the HTTP status isn't 2xx
        if r.status_code != requests.codes.ok:
            raise Exception("Status code is not 2xx")
        # TODO: return the text from the JSON field "response"
        else:
            return r.json()["response"]
        ...
    except requests.exceptions.ConnectionError as e:
        # TODO: return/print a clear message telling the user Ollama isn't running
        return f"Can't reach Ollama at {OLLAMA_URL}: {e}"
        ...

if __name__ == "__main__":
    print(ask("Explain what an LLM gateway is in one sentence."))