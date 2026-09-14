import pytest


from app.pipeline.product_pipeline import (
    extract_products,
    transform_products,
    validate_products,
    load_products,
    run_product_pipeline,
)


def test_extract_products():
    products = extract_products("data/products.json")

    assert len(products) == 4
    assert products[0]["name"] == "iPhone 15"
    assert products[0]["brand"] == "Apple"


def test_transform_products():
    products = [
        {
            "name": " iPhone 15 ",
            "description": " Smartphone Apple ",
            "category": " SMARTPHONE ",
            "brand": " Apple ",
            "price": 15000000,
        }
    ]

    transformed = transform_products(products)

    assert transformed[0]["name"] == "iPhone 15"
    assert transformed[0]["description"] == "Smartphone Apple"
    assert transformed[0]["category"] == "smartphone"
    assert transformed[0]["brand"] == "Apple"
    assert transformed[0]["price"] == 15000000.0
    
    
def test_validate_products():
    products = [
        {
            "name": "iPhone 15",
            "description": "Smartphone Apple",
            "category": "smartphone",
            "brand": "Apple",
            "price": 15000000,
        }
    ]

    validated = validate_products(products)

    assert validated == products


def test_validate_products_rejects_invalid_price():
    products = [
        {
            "name": "iPhone 15",
            "description": "Smartphone Apple",
            "category": "smartphone",
            "brand": "Apple",
            "price": 0,
        }
    ]

    with pytest.raises(ValueError):
        validate_products(products)
        
        
def test_load_products(db):
    products = [
        {
            "name": "Test iPhone",
            "description": "Test smartphone",
            "category": "smartphone",
            "brand": "Apple",
            "price": 10000000,
        },
        {
            "name": "Test Galaxy",
            "description": "Test smartphone Samsung",
            "category": "smartphone",
            "brand": "Samsung",
            "price": 9000000,
        },
    ]

    loaded_products = load_products(db, products)

    assert len(loaded_products) == 2
    assert loaded_products[0].name == "Test iPhone"
    assert loaded_products[1].brand == "Samsung"
    assert loaded_products[0].id is not None
    
    
def test_run_product_pipeline(db):
    loaded_products = run_product_pipeline(
        db,
        "data/products.json",
    )

    assert len(loaded_products) == 4
    assert loaded_products[0].id is not None
    
    
def test_load_products_does_not_create_duplicates(db):
    products = [
        {
            "name": "Test iPhone",
            "description": "Test smartphone",
            "category": "smartphone",
            "brand": "Apple",
            "price": 10000000,
        }
    ]

    first_load = load_products(db, products)
    second_load = load_products(db, products)

    assert len(first_load) == 1
    assert len(second_load) == 1

    assert first_load[0].id == second_load[0].id
    
def test_load_products_updates_existing_product(db):
    products = [
        {
            "name": "Test MacBook",
            "description": "Old description",
            "category": "laptop",
            "brand": "Apple",
            "price": 15000000,
        }
    ]

    first_load = load_products(db, products)

    updated_products = [
        {
            "name": "Test MacBook",
            "description": "New description",
            "category": "laptop",
            "brand": "Apple",
            "price": 18000000,
        }
    ]

    second_load = load_products(db, updated_products)

    assert first_load[0].id == second_load[0].id
    assert second_load[0].description == "New description"
    assert second_load[0].price == 18000000