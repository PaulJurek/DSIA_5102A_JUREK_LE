from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .database import BaseSQL
from .commande_produit import commande_produit  # Assurez-vous d'importer la table d'association

class Produit(BaseSQL):
    __tablename__ = "produits"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    nom = Column(String)
    description = Column(String)
    prix = Column(Float)
    imageurl = Column(String)

    # Définir la relation avec Commande via la table d'association
    commandes = relationship("Commande", secondary=commande_produit, back_populates="produits")
