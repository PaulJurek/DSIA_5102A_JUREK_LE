from typing import Optional, List
from uuid import uuid4

import jwt
from fastapi import HTTPException
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

import models.user as user
from schemas.commercant import Commercant
from services.auth import JWT_SECRET_KEY, JWT_SECRET_ALGORITHM


def create_commercant(db: Session, commercant: Commercant) -> user.Commercant:
    record = db.query(user.Commercant).filter(user.Commercant.pseudo == commercant.pseudo).first()
    if record:
        raise HTTPException(status_code=409, detail="Username already taken")

    db_user = user.Commercant(
        id=str(uuid4()), username=commercant.pseudo, password=commercant.mot_de_passe
    )
    db.add(db_user)
    db.commit()

    return db_user


def lister_tous_utilisateurs(db: Session) -> List[user.User]:
    return db.query(user.User).filter().all()


def get_user_by_id(db: Session, user_id: int) -> Optional[user.User]:
    return db.query(user.User).filter(user.User.id == user_id).first()


def get_user_id(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_SECRET_ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return user_id
    except InvalidTokenError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
