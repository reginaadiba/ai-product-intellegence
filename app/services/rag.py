from sqlalchemy.orm import Session

from app.services.embedding import generate_embedding
from app.repositories.product import search_by_embedding
from app.services.llm import generate_answer

def retrieve_products(
    db: Session,
    query: str,
    limit: int = 5,
    threshold: float = 0.3,
):
    query_embedding = generate_embedding(query)

    results = search_by_embedding(
        db=db,
        query_embedding=query_embedding,
        limit=limit,
        threshold=threshold,
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


def build_context(products: list[dict]) -> str:
    if not products:
        return "Tidak ada produk yang relevan."

    context_parts = []

    for product in products:
        context_parts.append(
            f"""
Produk: {product['name']}
Deskripsi: {product['description']}
Kategori: {product['category']}
Brand: {product['brand']}
Harga: Rp{product['price']:,.0f}
"""
        )

    return "\n".join(context_parts)

def generate_rag_answer(
    db: Session,
    query: str,
) -> str:
    products = retrieve_products(
        db=db,
        query=query,
    )

    context = build_context(products)

    prompt = f"""
Kamu adalah asisten produk.

Jawab pertanyaan pengguna hanya berdasarkan informasi
produk yang diberikan di bawah ini.

Jika informasi yang dibutuhkan tidak tersedia,
katakan bahwa informasi tersebut tidak tersedia.

Informasi produk:
{context}

Pertanyaan pengguna:
{query}

Berikan jawaban yang singkat dan jelas.
"""

    return generate_answer(prompt)