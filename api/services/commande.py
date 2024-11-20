# services/commande.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List  # Assurez-vous que List est importé
import models

# Récupérer toutes les commandes avec pagination
def get_liste_commandes(db: Session, skip: int = 0, limit: int = 10):
    commandes = db.query(models.Commande).offset(skip).limit(limit).all()
    if not commandes:
        raise HTTPException(status_code=404, detail="Aucune commande trouvée")
    return commandes

# Récupérer une commande par son ID
def get_commande_by_id(commande_id: str, db: Session):
    commande = db.query(models.Commande).filter(models.Commande.id == commande_id).first()
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return commande

def post_commande(produits_ids: List[str], db: Session):
    # Récupérer les produits depuis la base de données en fonction des IDs
    produits = db.query(models.Produit).filter(models.Produit.id.in_(produits_ids)).all()

    if not produits:
        raise HTTPException(status_code=404, detail="Produits non trouvés")

    # Calculer le total de la commande
    total = sum([produit.prix for produit in produits])

    # Créer la commande avec le total calculé
    nouvelle_commande = models.Commande(total=total)

    # Ajouter la commande dans la base de données
    db.add(nouvelle_commande)
    db.commit()
    db.refresh(nouvelle_commande)

    # Ajouter les produits à la commande (en utilisant la relation many-to-many)
    nouvelle_commande.produits = produits
    db.commit()

    return {"message": "Commande ajoutée avec succès", "commande": nouvelle_commande}

# Supprimer une commande
def delete_commande(commande_id: str, db: Session):
    try:
        commande = db.query(models.Commande).filter(models.Commande.id == commande_id).first()
        if not commande:
            raise HTTPException(status_code=404, detail="Commande non trouvée")
        
        db.delete(commande)
        db.commit()
        
        return {"message": "Commande supprimée avec succès"}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression de la commande")
