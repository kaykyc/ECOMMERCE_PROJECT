import unittest
import sqlite3

from mysqlx import DatabaseError
import sqlalchemy
import os

from unittest.mock import patch
from io import StringIO
from teste import TestProduto
from consultar_produto import consultar_produto
from deletar_produto import deletar_produto
from listar_produto import listar_produtos
from atualizar_produto import atualizar_produto
from teste import TestProduto

banco = sqlite3.connect('Produtos.db')
cursor = banco.cursor() 


""" DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite')
metadata = sqlalchemy.MetaData()

def configurar_banco(database_url = DATABASE_URL):
    engine = sqlalchemy.create_engine(database_url)
    metadata.drop_all(engine)
    metadata.create_all(engine)

if __name__ == "__main__":
    configurar_banco() """

# conectando...
conn = sqlite3.connect('Produtos.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, unidade INTEGER, nome TEXT, descricao TEXT, preco REAL)")
banco.commit()

print('Tabela criada com sucesso')