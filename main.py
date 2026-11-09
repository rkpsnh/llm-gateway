from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from hello_llm import ask, LLMUnavailableError, MODEL
import time
import json

app = FastAPI(title="LLM Gateway")

class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1)   

class ChatResponse(BaseModel):
    reply: str
    model: str

# Function to write to log file
def write_to_log(log_json):
    with open('./logs/requests.jsonl', 'w') as f:
        f.write(json.dumps(log_json) + '\n')

@app.get("/health")
def health():
    return {'status': "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    log = {
        "request_id": "", 
        "timestamp": "",
        "model": "",
        "prompt_chars":"", 
        "latency_ms": 0, #DONE
        "status_code": "",
        "prompt_tokens": 0
        }

    try:
        # Measure Latency
        start_time = time.time()
        response = ask(req.prompt)
        end_time = time.time()
        log["latency_ms"] = (end_time - start_time) * 1000

        write_to_log(log)
        return ChatResponse(reply=response, model=MODEL)
    
    except LLMUnavailableError as e:
        raise HTTPException(status_code=503, detail=str(e))
    
    finally:
         write_to_log(log)