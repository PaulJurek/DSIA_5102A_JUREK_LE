from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .database import BaseSQL
from .commande_produit import commande_produit  # Assurez-vous d'importer la table d'association

class Commande(BaseSQL):
    __tablename__ = "commandes"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    total = Column(Float)
    date_commande = Column(DateTime, default=datetime.utcnow)

    # Définir la relation avec Produit via la table d'association
    produits = relationship("Produit", secondary=commande_produit, back_populates="commandes")
