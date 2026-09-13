from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str
    category: str
    brand: str
    price: float = Field(gt=0)

class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    category: str | None = None
    brand: str | None = None
    price: float | None = Field(default=None, gt=0)

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    category: str
    brand: str
    price: float
    
class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    page: int
    limit: int
    total: int