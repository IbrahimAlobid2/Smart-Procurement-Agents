
from pydantic import BaseModel, Field ,HttpUrl ,validator
from typing import List ,Optional


class SuggestedSearchQueries(BaseModel):
    queries: List[str] = Field(
        ...,
        title="Suggested search queries to be passed to the search engine",
        min_items=1
    )



class SingleSearchResult(BaseModel):
    title: str = Field(..., title="Title of the product page result")
    url: HttpUrl = Field(..., title="The URL of the product page")
    content: str = Field(..., title="Brief snippet or page description")
    score: float = Field(..., ge=0.0, le=1.0, title="Confidence score (0-1)")
    search_query: str = Field(..., title="The search query that yielded this result")

class AllSearchResults(BaseModel):
    results: List[SingleSearchResult]
    
    
class ProductSpec(BaseModel):
    specification_name: str = Field(..., description="Name of the specification (e.g., RAM, Storage)")
    specification_value: str = Field(..., description="Value of the specification (e.g., 16GB, 1TB SSD)")


class SingleExtractedProduct(BaseModel):
    page_url: HttpUrl = Field(..., title="Original page URL", description="URL where the product was found")
    product_title: str = Field(..., title="Product title", description="The name/title of the product")
    product_image_url: HttpUrl = Field(..., title="Image URL", description="Direct link to the product image")
    product_url: HttpUrl = Field(..., title="Buy URL", description="URL for purchasing the product")

    product_current_price: float = Field(..., gt=0, title="Current price", description="Latest listed price of the product")
    product_original_price: Optional[float] = Field(
        default=None,
        title="Original price",
        description="Price before discount (if applicable)"
    )
    product_discount_percentage: Optional[float] = Field(
        default=None,
        title="Discount %",
        description="Calculated discount percent (if any), otherwise None"
    )

    product_specs: List[ProductSpec] = Field(
        ...,
        min_items=1,
        max_items=5,
        title="Key specifications",
        description="1–5 most relevant product specs (technical or functional)"
    )

    agent_recommendation_rank: int = Field(
        ...,
        ge=1,
        le=5,
        title="Recommendation Rank",
        description="Agent's ranking of this product out of 5 (5 = most recommended)"
    )
    agent_recommendation_notes: List[str] = Field(
        ...,
        min_items=1,
        title="Recommendation Notes",
        description="Reasoning behind recommendation (e.g., 'best value for money')"
    )

    @validator("product_original_price")
    def original_price_must_be_greater(cls, v, values):
        if v is not None and "product_current_price" in values:
            if v < values["product_current_price"]:
                raise ValueError("Original price must be higher than current price if provided.")
        return v


class AllExtractedProducts(BaseModel):
    products: List[SingleExtractedProduct] = Field(..., title="Extracted Products")




# ---------- Models for Scraper ----------
class ProductSpec_sec(BaseModel):
    specification_name: str
    specification_value: str

class SingleExtractedProduct_sec(BaseModel):
    page_url: HttpUrl
    product_title: str
    product_image_url: HttpUrl
    product_url: HttpUrl
    product_current_price: float
    product_original_price: float = None
    product_discount_percentage: float = None
    product_specs: List[ProductSpec_sec] = Field(..., min_items=1, max_items=5)
    agent_recommendation_rank: int = Field(..., ge=1, le=5)
    agent_recommendation_notes: List[str] = Field(..., min_items=1)

class AllExtractedProducts_sec(BaseModel):
    products: List[SingleExtractedProduct_sec]
