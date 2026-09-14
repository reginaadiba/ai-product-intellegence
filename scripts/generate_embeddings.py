from app.core.database import SessionLocal
from app.pipeline.embedding_pipeline import generate_product_embeddings


def main():
    db = SessionLocal()

    try:
        count = generate_product_embeddings(db)

        print(f"Generated embeddings for {count} products.")

    finally:
        db.close()


if __name__ == "__main__":
    main()