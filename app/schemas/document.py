from pydantic import BaseModel


class DocumentRequest(BaseModel):
    content: str


class DocumentResponse(BaseModel):
    response: str
