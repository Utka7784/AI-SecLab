from pydantic import BaseModel


# A Pydantic Model
class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str


