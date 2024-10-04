from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.dialects.postgresql import UUID
from database import BaseSQL


class model_User(BaseSQL):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    prenom = Column(String)
    nom = Column(String)
    surnom = Column(String, nullable=True)
    email = Column(String)
    date_naissance = Column(Date)
    adresse_numero = Column(Integer)
    adresse_rue = Column(String)
    adresse_ville = Column(String)  


#class model_Legumes(BaseSQL):
#    pass