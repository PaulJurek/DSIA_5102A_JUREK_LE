from sqlalchemy import Column, Float, DateTime, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .database import BaseSQL

class model_Panier(BaseSQL):
    __tablename__ = "PANIERS"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    nom_utilisateur = Column(String, ForeignKey('UTILISATEURS.nom_utilisateur'))
    nom_produit = Column(String, ForeignKey('PRODUITS.nom'))
    quantite = Column(Integer)
    prix_total = Column(Float)
    date_creation = Column(DateTime, default=datetime.now())
    date_modification = Column(DateTime, default=datetime.now())
    commande = Column(Integer, default=0)
