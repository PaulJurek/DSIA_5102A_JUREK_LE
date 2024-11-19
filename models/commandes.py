from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .database import BaseSQL


class Order(BaseSQL):
    __tablename__ = "COMMANDES"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    produit_id = Column(Integer, ForeignKey("legumes.id"))
    commercant_id = Column(Integer, ForeignKey("commercant.id"))
    status = Column(String, index=True)
    date_de_creation =  Column(Date)
    date_de_mise_a_jour = Column(Date)
    commercant = relationship("Commercant", back_populates="commandes")