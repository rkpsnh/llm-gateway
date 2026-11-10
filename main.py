from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from hello_llm import ask, LLMUnavailableError, MODEL
import time
import json
import uuid
import datetime

app = FastAPI(title="LLM Gateway")

class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1)   

class ChatResponse(BaseModel):
    reply: str
    model: str

# Function to write to log file
def write_to_log(log_json):
    with open('./logs/requests.jsonl', 'a') as f:
        f.write(json.dumps(log_json) + '\n')

@app.get("/health")
def health():
    return {'status': "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    log = {
        "request_id": "", 
        "timestamp": "",
        "model": MODEL,
        "prompt_chars":"", 
        "latency_ms": 0, #DONE
        "status_code": "",
        "prompt_tokens": 0
        }

    # Measure Latency
    start_time = time.time()

    # prompt chars
    char_count_req = len(req.prompt)
    log["prompt_chars"] = char_count_req

    try:
         # Generate ID
        log["request_id"] = str(uuid.uuid4())

        # Timestamp
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        log["timestamp"] = ts

        response = ask(req.prompt)

        # Status code
        log["status_code"] = 200

        # Prompt tokens

        return ChatResponse(reply=response, model=MODEL)
    
    except LLMUnavailableError as e:
        # Status code
        log["status_code"] = 503

        raise HTTPException(status_code=503, detail=str(e))
    
    finally:
        # Stop timer
        end_time = time.time()
        log["latency_ms"] = (end_time - start_time) * 1000
        write_to_log(log)