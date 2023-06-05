import unittest
import sqlite3

from unittest.mock import patch
from io import StringIO
from teste import TestProduto
from consultar_produto import consultar_produto
from deletar_produto import deletar_produto
from listar_produto import listar_produtos
from atualizar_produto import atualizar_produto
from teste import TestProduto

banco = sqlite3.connect('Banco.db')
cursor = banco.cursor()
