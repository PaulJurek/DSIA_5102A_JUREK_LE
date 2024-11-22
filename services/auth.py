import os

import jwt
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Dict, Union, List
from datetime import datetime, timedelta, timezone

from ..models import user as model_user
from ..schemas.users import User as schemas_user

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "should-be-an-environment-variable")
JWT_SECRET_ALGORITHM = os.getenv("JWT_SECRET_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def _encode_jwt(user: schemas_user) -> str:
    return jwt.encode(
        {
            "user_id": str(user.id),
        },
        JWT_SECRET_KEY,
        algorithm=JWT_SECRET_ALGORITHM,
    )

async def verify_authorization_header(
    authorization: str = Header(...),
) -> Dict[str, Union[int, Dict[str, Union[List[str], int, str]]]]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Manque header d'authentification")
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


async def get_user_id(authorization: str = Header(...)) -> str:
    auth = await verify_authorization_header(authorization)
    try:
        user_id = str(auth["user_id"])
    except KeyError:
        raise HTTPException(status_code=401, detail="Token invalide")
    return user_id


def generate_access_token(
    db: Session,
    user_login: schemas_user
):
    user = (
        db.query(model_user.User)
        .filter(
            model_user.User.pseudo == user_login.pseudo,
            model_user.User.mot_de_passe == user_login.mot_de_passe,
        )
        .first()
    ).update({"exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
})

    if not user:
        raise HTTPException(status_code=404, detail="Identifiant ou mot de passe incorrect")

    return _encode_jwt(user)
