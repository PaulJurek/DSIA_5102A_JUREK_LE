from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated


class Produit(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    nom: str
    description: Optional[str]
    prix_unite: float
    stock: int
    image_url: Optional[str]

    class Config:
        orm_mode = True
