from fastapi import HTTPException, Header
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import os
import jwt
from typing import Dict, Union, List
from datetime import datetime, timedelta, timezone
from models import model_Utilisateur
from schemas import schema_Utilisateur

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "should-be-an-environment-variable")
JWT_SECRET_ALGORITHM = os.getenv("JWT_SECRET_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Configuration de la sécurité des mots de passe avec CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _encode_jwt(utilisateur: schema_Utilisateur) -> str:
    return jwt.encode(
        {
            "nom_utilisateur": str(utilisateur.nom_utilisateur),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        },
        JWT_SECRET_KEY,
        algorithm=JWT_SECRET_ALGORITHM,
    )

async def verify_authorization_header(
    authorization: str = Header(...),
) -> Dict[str, Union[int, Dict[str, Union[List[str], int, str]]]]:
    try:
        auth = jwt.decode(
            authorization[7:],
            JWT_SECRET_KEY,
            algorithms=[JWT_SECRET_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError as err:
        raise HTTPException(status_code=401, detail=f"Token invalide: '{err}'")

    return auth


async def get_nom_utilisateur(authorization: str = Header(...)) -> str:
    auth = await verify_authorization_header(authorization)
    try:
        nom_utilisateur = str(auth["nom_utilisateur"])
    except KeyError:
        raise HTTPException(status_code=401, detail="Token invalide")
    return nom_utilisateur

def connexion(db: Session, utilisateur_connexion: schema_Utilisateur):
    utilisateur = db.query(model_Utilisateur).filter(model_Utilisateur.nom_utilisateur == utilisateur_connexion.nom_utilisateur).first()
    if not utilisateur:
        raise HTTPException(status_code=404, detail="L'utilisateur n'existe pas")
    if not pwd_context.verify(utilisateur_connexion.mot_de_passe, utilisateur.mot_de_passe):
        raise HTTPException(status_code=404, detail="Identifiant ou mot de passe incorrect")
    return _encode_jwt(utilisateur_connexion)
