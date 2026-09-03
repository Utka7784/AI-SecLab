from fastapi import FastAPI
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm import generate_response

app = FastAPI()

@app.get("/")
def index():
    return {"name": "First Date"}


@app.get("/health")
def new_index():
    return {
            "status": "ok"
            }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = generate_response(request.prompt)

    return ChatResponse(response=response)
