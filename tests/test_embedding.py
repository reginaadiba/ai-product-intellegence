from app.services.embedding import generate_embedding


def test_generate_embedding():
    text = "Smartphone Samsung dengan kamera canggih"

    embedding = generate_embedding(text)

    assert isinstance(embedding, list)
    assert len(embedding) == 384