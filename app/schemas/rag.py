from pydantic import BaseModel


class RAGRequest(BaseModel):
    query: str