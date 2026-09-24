from fastapi import FastAPI
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm import generate_response

from app.schemas.document import DocumentRequest, DocumentResponse
from app.services.document import summarize_document


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

@app.post("/document/summarize", response_model=DocumentResponse)
def summarize(request: DocumentRequest):
    response = summarize_document(request.content)
    return DocumentResponse(response=response)


