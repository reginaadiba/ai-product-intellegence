from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import engine
from app.routers.product import router as product_router

app = FastAPI(
    title="AI Product Intelligence API",
    description="Backend API for product data, semantic search, and AI-powered retrieval.",
    version="1.0.0",
)

app.include_router(product_router)

@app.get("/")
def root():
    return {
        "message": "AI Product Intelligence API is running"
    }
    
@app.get("/health/database")
def database_health():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {
            "database": result.scalar()
        }