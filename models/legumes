from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.dialects.postgresql import UUID
from .database import BaseSQL


class Legumes(BaseSQL):
   __tablename__ = "LEGUMES"

   id = Column(UUID(as_uuid=True), primary_key=True, index=True)
   nom = Column(String)
   nombre_commandes_par_personne = Column(Integer)
   nombre_commandes_totale = Column(Integer)
   stock_total = Column(Integer)
   date_de_creation =  Column(Date)
   date_de_mise_a_jour = Column(Date)