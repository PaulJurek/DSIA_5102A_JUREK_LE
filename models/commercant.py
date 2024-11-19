from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.dialects.postgresql import UUID
from .database import BaseSQL

class Commercant(BaseSQL):
    __tablename__ = "COMMERCANT"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    prenom = Column(String)
    nom = Column(String)
    pseudo = Column(String, nullable=True)
    email = Column(String)
    date_naissance = Column(Date, nullable=False)
    adresse_numero = Column(Integer)
    adresse_rue = Column(String)
    adresse_ville = Column(String)  
    mot_de_passe = Column(String)
    commandes = Column(Integer)
  
