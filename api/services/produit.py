from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from sqlalchemy.exc import SQLAlchemyError
import models, schemas

def get_liste_produits(db: Session, skip: int = 0, limit: int = 5) -> List[models.Produit]:
    records = db.query(models.Produit).filter().offset(skip).limit(limit).all()
    if not records:
        raise HTTPException(status_code=404, detail="Not Found")
    for record in records:
        record.id = str(record.id)
    return records

def get_produit_by_id(produit_id: str, db: Session) -> models.Produit:
    record = db.query(models.Produit).filter(models.Produit.id == produit_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found")
    record.id = str(record.id)
    return record

def get_produit_par_nom(nom: str, db: Session) -> List[models.Produit]:
    records = db.query(models.produit).filter(models.produit.nom == nom).all()
    for record in records:
        record.id = str(record.id)
    return records

def post_produit(nom: str, description: str, prix: float, imageurl: str, db: Session):
    try:
        # Créer une instance du produit avec les données envoyées via le formulaire
        nouveau_produit = models.Produit(
            nom=nom,  # On passe la variable 'nom' directement ici
            description=description,  # Idem pour 'description'
            prix=prix,  # Idem pour 'prix'
            imageurl=imageurl  # Idem pour 'imageurl'
        )
        
        # Ajouter à la base de données
        db.add(nouveau_produit)
        db.commit()
        db.refresh(nouveau_produit)  # Rafraîchir l'objet pour obtenir l'ID généré
        
        return {"message": "Produit ajouté avec succès", "produit": nouveau_produit}

    except SQLAlchemyError as e:
        db.rollback()  # Annuler la transaction en cas d'erreur
        raise HTTPException(status_code=500, detail="Erreur lors de l'ajout du produit")

def update_produit(produit_id: str, updated_data: dict, db: Session):
    try:
        produit = db.query(models.Produit).filter(models.Produit.id == produit_id).first()
        if not produit:
            raise HTTPException(status_code=404, detail="Produit non trouvé")

        # Mise à jour des champs
        for key, value in updated_data.items():
            setattr(produit, key, value)

        db.commit()
        db.refresh(produit)
        return produit
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erreur lors de la modification")

def delete_produit(produit_id: str, db: Session):
    try:
        produit = db.query(models.Produit).filter(models.Produit.id == produit_id).first()
        if not produit:
            raise HTTPException(status_code=404, detail="Produit non trouvé")

        db.delete(produit)
        db.commit()
        return {"message": "Produit supprimé avec succès"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression")