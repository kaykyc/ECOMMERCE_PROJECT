import ormar
import re
from pydantic import validator
from sqlalchemy.sql.expression import table
from config import database, metadata

class Produto(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename = "produtos"

    cod: int = ormar.Integer(primary_key=True, name="cod")
    nome: str = ormar.String(max_length=100)
    preco: str = ormar.String(max_length=10)
    qnt: int = ormar.Integer()
