from app.core.database import SessionLocal
from app.services.rag import generate_rag_answer


def main():
    query = "Saya mencari smartphone dengan kamera bagus"

    db = SessionLocal()

    try:
        answer = generate_rag_answer(
            db=db,
            query=query,
        )

        print("\n=== AI ANSWER ===")
        print(answer)

    finally:
        db.close()


if __name__ == "__main__":
    main()