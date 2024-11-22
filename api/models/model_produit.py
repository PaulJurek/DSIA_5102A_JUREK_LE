from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from .database import BaseSQL


class Produit(BaseSQL):
    __tablename__ = "PRODUITS"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    nom = Column(String)
    description = Column(String)
    prix_unite = Column(Float)
    stock = Column(Integer)
    image_url = Column(String)