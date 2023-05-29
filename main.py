import sqlite3
import unittest

from typing import Union
from fastapi import FastAPI


class TestAdicionarProduto(unittest.TestCase):
    def test_adicionar_produto(self):
        unidade = 5
        nome = "Caneta"
        descricao = "azul"
        preco = 10.0

        adicionar_produto(unidade, nome, descricao, preco)

        # Assert if the product is added successfully by querying the database
        cursor.execute("SELECT * FROM produtos WHERE nome=?", (nome,))
        result = cursor.fetchone()
        if result is None:
            print(f"Failed to add product with name: {nome}")
        else:
            self.assertEqual(result[1], unidade, f"Expected unidade: {unidade}, Actual unidade: {result[1]}")
            self.assertEqual(result[2], nome, f"Expected nome: {nome}, Actual nome: {result[2]}")
            self.assertEqual(result[3], descricao, f"Expected descricao: {descricao}, Actual descricao: {result[3]}")
            self.assertEqual(result[4], preco, f"Expected preco: {preco}, Actual preco: {result[4]}")

def runTests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAdicionarProduto)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    runTests()