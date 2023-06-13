from typing import List, Optional
from pydantic import BaseModel

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    preco: Optional [str]= None
    qnt: Optional[int] = None