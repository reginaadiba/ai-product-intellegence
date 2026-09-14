from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

# load otak/model embedding yang akan digunakan
model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

print("Embedding model loaded!")

# ubah kalimat ini menjadi angka-angka yang mewakili maknanya
def generate_embedding(text: str) -> list[float]:
    embedding = model.encode(text)

    return embedding.tolist()