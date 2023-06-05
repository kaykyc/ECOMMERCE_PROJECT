import unittest
import sqlite3
from unittest.mock import patch
from io import StringIO

from adicionar_produto import adicionar_produto
from consultar_produto import consultar_produto
from deletar_produto import deletar_produto
from listar_produto import listar_produtos
from atualizar_produto import atualizar_produto

class TestProduto(unittest.TestCase):
    def setUp(self):
        self.banco = sqlite3.connect(':memory:')
        self.cursor = self.banco.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, unidade INTEGER, nome TEXT, descricao TEXT, preco REAL)")
        self.banco.commit()

    def tearDown(self):
        self.cursor.execute("DROP TABLE IF EXISTS produtos")
        self.banco.close()

    def test_adicionar_produto(self):
        unidade = 5
        nome = "Caneta"
        descricao = "azul"
        preco = 10.0

        adicionar_produto(unidade, nome, descricao, preco, self.cursor, self.banco)

        # Assert if the product is added successfully by querying the database
        self.cursor.execute("SELECT * FROM produtos WHERE nome=?", (nome,))
        result = self.cursor.fetchone()
        if result is None:
            print(f"Failed to add product with name: {nome}")
        else:
            self.assertEqual(result[1], unidade, f"Expected unidade: {unidade}, Actual unidade: {result[1]}")
            self.assertEqual(result[2], nome, f"Expected nome: {nome}, Actual nome: {result[2]}")
            self.assertEqual(result[3], descricao, f"Expected descricao: {descricao}, Actual descricao: {result[3]}")
            self.assertEqual(result[4], preco, f"Expected preco: {preco}, Actual preco: {result[4]}")

    def test_deletar_produto(self):
        unidade = 5
        nome = "Caneta"
        descricao = "azul"
        preco = 10.0

        adicionar_produto(unidade, nome, descricao, preco, self.cursor, self.banco)

        # Get the ID of the added product
        self.cursor.execute("SELECT id FROM produtos WHERE nome=?", (nome,))
        id_produto = self.cursor.fetchone()[0]

        # Delete the product
        deletar_produto(id_produto, self.cursor, self.banco)

        # Assert if the product is deleted by querying the database
        self.cursor.execute("SELECT * FROM produtos WHERE id=?", (id_produto,))
        result = self.cursor.fetchone()
        self.assertIsNone(result, "Failed to delete the product")

    def test_consultar_produto(self):
        unidade = 5
        nome = "Caneta"
        descricao = "azul"
        preco = 10.0

        adicionar_produto(unidade, nome, descricao, preco, self.cursor, self.banco)

        # Get the ID of the added product
        self.cursor.execute("SELECT id FROM produtos WHERE nome=?", (nome,))
        id_produto = self.cursor.fetchone()[0]

        with patch('builtins.input', side_effect=['n']):
            consultar_produto(id_produto, self.cursor)

        with patch('builtins.input', side_effect=['s', '6', 'Lápis', 'preto', '5.0']):
            consultar_produto(99, self.cursor)

        # Assert if the product is queried successfully by printing its details
        with patch('sys.stdout', new_callable=StringIO) as mocked_output:
            with patch('builtins.input', side_effect=['s', '10', 'Borracha', 'apaga bem', '3.5']):
                consultar_produto(id_produto, self.cursor)
            expected_output = "Produto encontrado:\nID: {}\nUnidade: {}\nNome: {}\nDescrição: {}\nPreço: {}\n".format(
                id_produto, unidade, nome, descricao, preco)
            self.assertEqual(mocked_output.getvalue(), expected_output)

    def test_atualizar_produto(self):
        unidade = 5
        nome = "Caneta"
        descricao = "azul"
        preco = 10.0

        adicionar_produto(unidade, nome, descricao, preco, self.cursor, self.banco)

        # Get the ID of the added product
        self.cursor.execute("SELECT id FROM produtos WHERE nome=?", (nome,))
        id_produto = self.cursor.fetchone()[0]

        with patch('builtins.input', side_effect=['n']):
            atualizar_produto(id_produto, "Lápis", "preto", 5.0, self.cursor, self.banco)

        with patch('builtins.input', side_effect=['s', '6', 'Lápis', 'preto', '5.0']):
            atualizar_produto(99, "Caneta", "azul", 10.0, self.cursor, self.banco)

        # Assert if the product is updated successfully by querying the database
        self.cursor.execute("SELECT * FROM produtos WHERE id=?", (id_produto,))
        result = self.cursor.fetchone()
        if result is None:
            print(f"Failed to update product with ID: {id_produto}")
        else:
            self.assertEqual(result[2], "Lápis", f"Expected nome: Lápis, Actual nome: {result[2]}")
            self.assertEqual(result[3], "preto", f"Expected descricao: preto, Actual descricao: {result[3]}")
            self.assertEqual(result[4], 5.0, f"Expected preco: 5.0, Actual preco: {result[4]}")

    def test_listar_produtos(self):
        unidade = 5
        nome = "Caneta"
        descricao = "azul"
        preco = 10.0

        adicionar_produto(unidade, nome, descricao, preco, self.cursor, self.banco)

        with patch('builtins.input', side_effect=['n']):
            listar_produtos(self.cursor)

        with patch('builtins.input', side_effect=['s', '6', 'Lápis', 'preto', '5.0']):
            listar_produtos(self.cursor)

        # Assert if the product is listed successfully by printing the list
        with patch('sys.stdout', new_callable=StringIO) as mocked_output:
            with patch('builtins.input', side_effect=['s', '10', 'Borracha', 'apaga bem', '3.5']):
                listar_produtos(self.cursor)
            expected_output = "Lista de produtos:\nID: {}\nUnidade: {}\nNome: {}\nDescrição: {}\nPreço: {}\n----------------------\n".format(
                1, unidade, nome, descricao, preco)
            self.assertEqual(mocked_output.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()
