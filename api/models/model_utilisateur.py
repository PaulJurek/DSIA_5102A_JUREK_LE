from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime
from .database import BaseSQL

class model_Utilisateur(BaseSQL):
    __tablename__ = "UTILISATEURS"

    nom_utilisateur = Column(String, primary_key=True)
    mot_de_passe = Column(String)
    admin = Column(Integer, default=0)
    date_creation = Column(DateTime, default=datetime.now())
    date_modification = Column(DateTime, default=datetime.now())