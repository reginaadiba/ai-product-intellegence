import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.product import Product

def extract_products(file_path: str) -> list[dict]:
    # Menentukan lokasi file
    path = Path(file_path)

    # Membuka file JSON
    with path.open("r", encoding="utf-8") as file:
        products = json.load(file)

    return products

def transform_products(products: list[dict]) -> list[dict]:
    transformed_products = []

    for product in products:
        transformed_product = {
            "name": product["name"].strip(),
            "description": product["description"].strip(),
            "category": product["category"].strip().lower(),
            "brand": product["brand"].strip(),
            "price": float(product["price"]),
        }

        transformed_products.append(transformed_product)

    return transformed_products

def validate_products(products: list[dict]) -> list[dict]:
    required_fields = [
        "name",
        "description",
        "category",
        "brand",
        "price",
    ]

    for index, product in enumerate(products):
        for field in required_fields:
            if field not in product:
                raise ValueError(
                    f"Product at index {index} is missing field: {field}"
                )

            if product[field] is None:
                raise ValueError(
                    f"Product at index {index} has empty field: {field}"
                )

        if not product["name"].strip():
            raise ValueError(
                f"Product at index {index} has empty name"
            )

        if not product["description"].strip():
            raise ValueError(
                f"Product at index {index} has empty description"
            )

        if not product["category"].strip():
            raise ValueError(
                f"Product at index {index} has empty category"
            )

        if not product["brand"].strip():
            raise ValueError(
                f"Product at index {index} has empty brand"
            )

        if product["price"] <= 0:
            raise ValueError(
                f"Product at index {index} must have price greater than 0"
            )

    return products

# def load_products(
#     db: Session,
#     products: list[dict],
# ) -> list[Product]:
#     created_products = []

#     for product_data in products:
#         product = Product(**product_data)

#         db.add(product)
#         created_products.append(product)

#     db.commit()

#     for product in created_products:
#         db.refresh(product)

#     return created_products

def load_products(
    db: Session,
    products: list[dict],
) -> list[Product]:
    loaded_products = []

    for product_data in products:
        existing_product = (
            db.query(Product)
            .filter(
                Product.name == product_data["name"],
                Product.brand == product_data["brand"],
            )
            .first()
        )

        if existing_product:
            existing_product.description = product_data["description"]
            existing_product.category = product_data["category"]
            existing_product.price = product_data["price"]

            loaded_products.append(existing_product)
        else:
            product = Product(**product_data)

            db.add(product)
            loaded_products.append(product)

    db.commit()

    for product in loaded_products:
        db.refresh(product)

    return loaded_products

def run_product_pipeline(
    db: Session,
    file_path: str,
) -> list[Product]:
    products = extract_products(file_path)

    products = transform_products(products)

    products = validate_products(products)

    products = load_products(db, products)

    return products