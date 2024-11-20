from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class Commande(BaseModel):
    total: float
    produits_ids: List[UUID]  # Liste des IDs des produits dans la commande

    class Config:
        orm_mode = True  # Permet de convertir les objets SQLAlchemy en objets Pydantic
