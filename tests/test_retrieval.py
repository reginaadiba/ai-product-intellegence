from app.services.rag import retrieve_products


def test_retrieve_products():
    results = retrieve_products("sepatu untuk olahraga")

    assert len(results) > 0
    assert results[0]["name"] == "Nike Air Max"