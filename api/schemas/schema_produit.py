from typing import Optional
from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated


class schema_Produit(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    nom: str
    description: Optional[str]
    prix: Optional[float]
    imageurl: Optional[str]

    class Config:
        orm_mode = True
