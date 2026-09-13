from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
)
from app.services import product as product_service


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201,
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    return product_service.create_product(
        db,
        product,
    )


# @router.get(
#     "/",
#     response_model=list[ProductResponse],
# )
# def get_products(
#     db: Session = Depends(get_db),
# ):
#     return product_service.get_products(db)

@router.get(
    "/",
    response_model=ProductListResponse,
)
def get_products(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
    category: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    products, total = product_service.get_products(
        db=db,
        page=page,
        limit=limit,
        search=search,
        category=category,
    )

    return {
        "items": products,
        "page": page,
        "limit": limit,
        "total": total,
    }

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = product_service.get_product(
        db,
        product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
):
    product = product_service.update_product(
        db,
        product_id,
        product_data,
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    deleted = product_service.delete_product(
        db,
        product_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return {
        "message": "Product deleted successfully"
    }