from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import List
from datetime import datetime
from models import model_Panier
from models import model_Utilisateur
from schemas import schema_Panier

def get_liste_paniers_utilisateur(db: Session, nom_utilisateur: str) -> List[model_Panier]:
    db.query(model_Utilisateur).filter(model_Utilisateur.nom_utilisateur==nom_utilisateur).first()
    records = db.query(model_Panier).filter(model_Panier.nom_utilisateur==nom_utilisateur, model_Panier.commande==0).all()
    if not records:
        raise HTTPException(status_code=404, detail="Not Found")
    grand_total = 0
    for record in records:
        record.id = str(record.id)
        record.nom_produit = record.nom_produit
        grand_total += record.quantite * record.prix_total
    return records, grand_total

def get_panier_by_id(db: Session, panier_id: str):
    record = db.query(model_Panier).filter(model_Panier.id==panier_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found")
    record.id = str(record.id)
    return record

def post_produit_panier(db: Session, panier: schema_Panier):
    try:
        db_panier = model_Panier(
            nom_utilisateur = panier.nom_utilisateur,
            nom_produit = panier.nom_produit,
            quantite = panier.quantite,
            prix_total = panier.prix_total
        )

        db.add(db_panier)
        db.commit()
        db.refresh(db_panier)

        return db_panier
    
    except SQLAlchemyError as e:
        db.rollback()  # Annuler la transaction en cas d'erreur
        raise HTTPException(status_code=500, detail="Erreur lors de l'ajout du panier")

def delete_panier(panier_id: str, db: Session):
    try:
        panier = db.query(model_Panier).filter(model_Panier.id == panier_id).first()
        if not panier:
            raise HTTPException(status_code=404, detail="Panier non trouvé")
        
        db.delete(panier)
        db.commit()

        return
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression du panier")
    
def commander(db: Session, nom_utilisateur: str):
    db.query(model_Utilisateur).filter(model_Utilisateur.nom_utilisateur==nom_utilisateur).first()
    records = db.query(model_Panier).filter(model_Panier.nom_utilisateur==nom_utilisateur, model_Panier.commande==0).all()
    if not records:
        raise HTTPException(status_code=404, detail="Not Found")
    for record in records:
        record.commande = 1
        record.date_modification = datetime.now()
        db.commit()
        db.refresh(record)
    return records