from pydantic import BaseModel
from typing_extensions import Annotated


class schema_Panier(BaseModel):
    nom_produit: str
    nom_utilisateur: str
    quantite: int
    prix_total: float

    class Config:
        orm_mode = True
