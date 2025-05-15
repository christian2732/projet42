# Objectif : Définir le modèle de données d’un indice boursier

from pydantic import BaseModel

class Index(BaseModel):
    name: str
    value: float
