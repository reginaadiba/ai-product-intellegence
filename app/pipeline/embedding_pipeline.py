from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.services.embedding import generate_embedding


def generate_product_embeddings(db: Session) -> int:
    products = db.scalars(
        select(Product).where(Product.embedding.is_(None))
    ).all()

    for product in products:
        text = f"{product.name}. {product.description}"

        product.embedding = generate_embedding(text)

    db.commit()

    return len(products)