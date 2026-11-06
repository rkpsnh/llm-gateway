from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from hello_llm import ask, LLMUnavailableError, MODEL

app = FastAPI(title="LLM Gateway")

class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1)   

class ChatResponse(BaseModel):
    reply: str
    model: str
    ...

@app.get("/health")
def health():
    return {'status': "ok"}
    ...

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        
        response = ask(req.prompt)

        return ChatResponse(reply=response, model=MODEL)
    except LLMUnavailableError as e:

        raise HTTPException(status_code=503, detail=str(e))
        ...