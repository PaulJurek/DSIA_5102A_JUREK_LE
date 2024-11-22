from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from models import model_Panier
from models import model_Utilisateur

def get_liste_commandes_utilisateur(db: Session, nom_utilisateur: str) -> List[model_Panier]:
    db.query(model_Utilisateur).filter(model_Utilisateur.nom_utilisateur==nom_utilisateur).first()
    records = db.query(model_Panier).filter(model_Panier.nom_utilisateur==nom_utilisateur, model_Panier.commande==1).all()
    if not records:
        raise HTTPException(status_code=404, detail="Not Found")
    for record in records:
        record.id = str(record.id)
        record.nom_produit = record.nom_produit
    return records

def get_commandes(db: Session) -> List[model_Panier]:
    records = db.query(model_Panier).filter(model_Panier.commande==1).all()
    if not records:
        raise HTTPException(status_code=404, detail="Not Found")
    for record in records:
        record.id = str(record.id)
        record.nom_produit = record.nom_produit
    return records