
from pydantic import BaseModel, Field
from typing import List


class SuggestedSearchQueries(BaseModel):
    queries: List[str] = Field(
        ...,
        title="Suggested search queries to be passed to the search engine",
        min_items=1
    )
