from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from hello_llm import ask, LLMUnavailableError, LLMTimeOutError, LLMUpstreamError, MODEL
import time
import json
import uuid
import datetime
import os
os.makedirs("logs", exist_ok=True)

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
        "prompt_tokens": None,
        "completion_tokens": None,
        "error": None
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


        # Ask
        response = ask(req.prompt)
        reply = response["reply"]

        # Status code
        log["status_code"] = 200

        # Prompt tokens
        log["prompt_tokens"] = response["prompt_tokens"]

        log["completion_tokens"] = response["completion_tokens"]
        return ChatResponse(reply=reply, model=MODEL)
    
    except LLMUnavailableError as e:
        # Status code
        log["status_code"] = 503

        log["error"] = str(e)
        raise HTTPException(status_code=503, detail="LLM backend unavailable")
    
    except LLMTimeOutError as e:
        # Status code
        log["status_code"] = 504
        log["error"] = str(e)
        raise HTTPException(status_code=504, detail="LLM backend timed out")
    
    except LLMUpstreamError as e:
        log["status_code"] = 502
        log["error"] = str(e)
        raise HTTPException(status_code=502, detail="LLM backend returned an error")
    
    finally:
        # Stop timer
        end_time = time.time()
        log["latency_ms"] = (end_time - start_time) * 1000
        write_to_log(log)