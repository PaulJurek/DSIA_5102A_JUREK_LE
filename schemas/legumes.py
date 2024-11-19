from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated


class Legume(BaseModel):
    id: Annotated[int, Field(default_factory=lambda: uuid4().hex)]
    nom: str
    nombre_commandes_par_personne: int
    nombre_commandes_totale: int
    stock_total: int
    date_de_creation: Annotated[datetime, Field(default_factory=lambda: datetime.now())]
    date_de_mise_a_jour: Annotated[datetime, Field(default_factory=lambda: datetime.now())]

    class Config:
        orm_mode = True
