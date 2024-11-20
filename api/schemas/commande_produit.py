from pydantic import BaseModel
from uuid import UUID

class CommandeProduit(BaseModel):
    commande_id: UUID
    produit_id: UUID

    class Config:
        orm_mode = True
