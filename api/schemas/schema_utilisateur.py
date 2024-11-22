from pydantic import BaseModel

class schema_Utilisateur(BaseModel):
    nom_utilisateur: str
    mot_de_passe: str

    class Config:
        orm_mode = True
