from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.product import Product


def create_product(
    db: Session,
    product: Product,
) -> Product:
    db.add(product)
    db.commit()
    db.refresh(product)

    return product


# def get_products(
#     db: Session,
# ) -> list[Product]:
#     statement = select(Product)

#     result = db.execute(statement)

#     return list(result.scalars().all())

def get_products(
    db: Session,
    page: int,
    limit: int,
    search: str | None = None,
    category: str | None = None,
):
    statement = select(Product)

    if search:
        search_pattern = f"%{search}%"

        statement = statement.where(
            Product.name.ilike(search_pattern)
            | Product.description.ilike(search_pattern)
            | Product.brand.ilike(search_pattern)
        )

    if category:
        statement = statement.where(
            Product.category.ilike(category)
        )
    # jika category ada tabel tersendiri gimana?

    count_statement = select(func.count()).select_from(
        statement.subquery()
    )

    total = db.execute(count_statement).scalar_one()

    offset = (page - 1) * limit

    statement = (
        statement
        .order_by(Product.id.desc())
        .offset(offset)
        .limit(limit)
    )

    result = db.execute(statement)

    products = list(result.scalars().all())

    return products, total


def search_by_embedding(
    db,
    query_embedding: list[float],
    limit: int = 10,
    threshold: float = 0.3,
):
    distance = Product.embedding.cosine_distance(query_embedding)
    # Similarity tinggi = semakin mirip
    # distance kecil → semakin mirip
    # distance besar → semakin tidak mirip
    
    stmt = (
        select(Product, distance.label("distance"))
        .where(
            Product.embedding.is_not(None),
            distance <= (1 - threshold),
        )
        .order_by(
            distance
        )
        .limit(limit)
    )

    # return db.scalars(stmt).all()
    return db.execute(stmt).all()


def get_product_by_id(
    db: Session,
    product_id: int,
) -> Product | None:
    statement = select(Product).where(
        Product.id == product_id
    )

    result = db.execute(statement)

    return result.scalar_one_or_none()


def update_product(
    db: Session,
    product: Product,
) -> Product:
    db.commit()
    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product: Product,
) -> None:
    db.delete(product)
    db.commit()