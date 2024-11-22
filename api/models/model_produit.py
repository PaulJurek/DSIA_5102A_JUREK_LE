from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .database import BaseSQL

class model_Produit(BaseSQL):
    __tablename__ = "PRODUITS"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    nom = Column(String, nullable=False, unique=True)
    description = Column(String)
    prix = Column(Float)
    imageurl = Column(String)
    date_creation = Column(DateTime, default=datetime.now())
    date_modification = Column(DateTime, default=datetime.now())