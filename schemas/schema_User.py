from pydantic import BaseModel, field_validator
from datetime import datetime, date
from typing import Optional
import re

class schema_User(BaseModel):

    prenom: str
    nom: str
    surnom: Optional[str]
    email:str
    date_naissance: str
    adresse_numero: int
    adresse_rue: str
    adresse_ville: str
    mot_de_passe: str

    @field_validator('prenom', 'nom', 'surnom')
    def validator_prenom_nom_surnom(cls, v, info):
        if not v.strip():
            raise ValueError(f'Le {info.field_name} ne doit pas être vide')
        if len(v) > 32:
            raise ValueError(f'Le {info.field_name} ne doit pas dépasser les 32 caractères')
        regex = ''
        if info.field_name == 'prenom':
            regex = r"^[A-Za-zÀ-ÿ- ]+$"
        if info.field_name == 'nom':
            regex = r"^[A-Za-zÀ-ÿ' -]+$"
        if re.match(regex, v):
            return v
        raise ValueError(f'Le {info.field_name} est invalide')
    
    @field_validator('email')
    def validator_email(cls, v):
        if not v.strip():
            raise ValueError("L'email ne doit pas être vide")
        regex_email = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(regex_email, v):
            raise ValueError("L'email est invalide")
        return v
        
    
    @field_validator('date_naissance')
    def validator_date_naissance(cls, v):
        try:
            date_naissance = datetime.strptime(v, '%d/%m/%Y').date()
        except ValueError:
            raise ValueError('La date de naissance doit être au format JJ/MM/AAAA')
        aujourdhui = date.today()
        age = aujourdhui.year - date_naissance.year - ((aujourdhui.month, aujourdhui.day) < (date_naissance.month, date_naissance.day))
        if age < 0:
            raise ValueError("La date est invalide")
        if age < 13:
            raise ValueError("L'utilisateur doit avoir au moins 13 ans")
        return date_naissance

    @field_validator('adresse_numero', 'adresse_rue', 'adresse_ville')
    def validator_adresse(cls,v,info):
        if info.field_name == 'adresse_numero':
            return v
        if not v.strip():
            raise ValueError(f'Le {info.field_name} ne doit pas être vide')
        regex = ''
        if info.field_name == 'adresse_rue':
            regex = r"^[A-Za-zÀ-ÿ' -]+$"
        if info.field_name == 'adresse_ville':
            regex = r"^[A-Za-zÀ-ÿ' -]+$"
        if not re.match(regex,v):
            raise ValueError(f'Le {info.field_name} est invalide')
        return v