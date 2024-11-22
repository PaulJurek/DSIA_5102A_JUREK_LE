from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from typing import List, Optional
from schemas import schema_Utilisateur
from models import model_Utilisateur

# Configuration de la sécurité des mots de passe avec CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_utilisateurs(db: Session) -> List[model_Utilisateur]:
    return db.query(model_Utilisateur).filter().all()

def get_utilisateur_par_nom(db: Session, nom_utilisateur: str) -> Optional[model_Utilisateur]:
    return db.query(model_Utilisateur).filter(model_Utilisateur.nom_utilisateur == nom_utilisateur).first()

def post_utilisateur(db: Session, utilisateur_inscription: schema_Utilisateur):
    record = db.query(model_Utilisateur).filter(model_Utilisateur.nom_utilisateur == utilisateur_inscription.nom_utilisateur).first()
    if record:
        raise HTTPException(status_code=409, detail="Username already taken")
    
    db_utilisateur = model_Utilisateur(
        nom_utilisateur = utilisateur_inscription.nom_utilisateur,
        mot_de_passe = pwd_context.hash(utilisateur_inscription.mot_de_passe)
    )

    db.add(db_utilisateur)
    db.commit()

    return db_utilisateur

def utilisateur_est_admin(db: Session, nom_utilisateur: str):
    utilisateur = db.query(model_Utilisateur).filter(model_Utilisateur.nom_utilisateur == nom_utilisateur).first()
    return utilisateur.admin == 1