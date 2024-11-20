from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .database import BaseSQL

# Table d'association entre Commande et Produit
commande_produit = Table(
    "commande_produit", BaseSQL.metadata,
    Column("commande_id", UUID(as_uuid=True), ForeignKey("commandes.id"), primary_key=True),
    Column("produit_id", UUID(as_uuid=True), ForeignKey("produits.id"), primary_key=True)
)
