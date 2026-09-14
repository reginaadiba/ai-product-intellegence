from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories import product as product_repository
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.embedding import generate_embedding
from app.repositories.product import search_by_embedding


def create_product(
    db: Session,
    product_data: ProductCreate,
) -> Product:

    product = Product(
        **product_data.model_dump()
    )

    return product_repository.create_product(
        db,
        product,
    )


# def get_products(
#     db: Session,
# ) -> list[Product]:

#     return product_repository.get_products(db)

def get_products(
    db: Session,
    page: int,
    limit: int,
    search: str | None = None,
    category: str | None = None,
):
    return product_repository.get_products(
        db=db,
        page=page,
        limit=limit,
        search=search,
        category=category,
    )


def get_product(
    db: Session,
    product_id: int,
) -> Product | None:

    return product_repository.get_product_by_id(
        db,
        product_id,
    )
    
    
def semantic_search(
    db,
    query: str,
    limit: int = 10,
    threshold: float = 0.3,
):
    query_embedding = generate_embedding(query)

    results = search_by_embedding(
        db,
        query_embedding,
        limit,
        threshold,
    )

    return [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "brand": product.brand,
            "price": product.price,
            "similarity": round(1 - distance, 4),
        }
        for product, distance in results
    ]
    
    
def update_product(
    db: Session,
    product_id: int,
    product_data: ProductUpdate,
) -> Product | None:

    product = product_repository.get_product_by_id(
        db,
        product_id,
    )

    if product is None:
        return None

    update_data = product_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(product, field, value)

    return product_repository.update_product(
        db,
        product,
    )


def delete_product(
    db: Session,
    product_id: int,
) -> bool:

    product = product_repository.get_product_by_id(
        db,
        product_id,
    )

    if product is None:
        return False

    product_repository.delete_product(
        db,
        product,
    )

    return True