from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import List
from datetime import datetime
from models import model_Produit
from schemas import schema_Produit

def get_liste_produits(db: Session, skip: int = 0, limit: int = 5) -> List[model_Produit]:
    records = db.query(model_Produit).filter().offset(skip).limit(limit).all()
    if not records:
        raise HTTPException(status_code=404, detail="Not Found")
    for record in records:
        record.id = str(record.id)
    return records

def get_produit_by_id(produit_id: str, db: Session) -> model_Produit:
    record = db.query(model_Produit).filter(model_Produit.id == produit_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found")
    record.id = str(record.id)
    return record

def post_produit(produit: schema_Produit, db: Session):
    try:
        # Créer une instance du produit avec les données envoyées via le formulaire
        db_produit = model_Produit(
            nom=produit.nom,  # On passe la variable 'nom' directement ici
            description=produit.description,  # Idem pour 'description'
            prix=produit.prix,  # Idem pour 'prix'
            imageurl=produit.imageurl  # Idem pour 'imageurl'
        )
        
        # Ajouter à la base de données
        db.add(db_produit)
        db.commit()
        db.refresh(db_produit)  # Rafraîchir l'objet pour obtenir l'ID généré
        
        return db_produit

    except SQLAlchemyError as e:
        db.rollback()  # Annuler la transaction en cas d'erreur
        raise HTTPException(status_code=500, detail="Erreur lors de l'ajout du produit")

def update_produit(produit: schema_Produit, db: Session):
    try:
        db_produit = db.query(model_Produit).filter(model_Produit.id == produit.id).first()
        if not db_produit:
            raise HTTPException(status_code=404, detail="Produit non trouvé")

        # Mise à jour des champs
        for var, value in vars(produit).items():
            setattr(db_produit, var, value) if value else None
        db_produit.date_modification = datetime.now()

        db.commit()
        db.refresh(db_produit)

        return db_produit
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erreur lors de la modification du produit")

def delete_produit(produit_id: str, db: Session):
    try:
        produit = db.query(model_Produit).filter(model_Produit.id == produit_id).first()
        if not produit:
            raise HTTPException(status_code=404, detail="Produit non trouvé")

        db.delete(produit)
        db.commit()

        return
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression du produit")
