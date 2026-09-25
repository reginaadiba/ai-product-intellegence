from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.rag import RAGRequest
from app.services.rag import generate_rag_answer


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.post("/ask")
def ask_product(request: RAGRequest, db: Session = Depends(get_db)):
    answer = generate_rag_answer(
        db=db,
        query=request.query,
    )

    return {
        "query": request.query,
        "answer": answer,
    }