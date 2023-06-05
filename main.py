import unittest
import sqlite3
from unittest.mock import patch
from io import StringIO

banco = sqlite3.connect('Banco.db')
cursor = banco.cursor()

def adicionar_produto(unidade, nome, descricao, preco, cursor, banco):
    while True:
        try:
            unidade = int(unidade)
            if unidade <= 0:
                print("O estoque não pode ser negativo")
                unidade = input("Digite um número válido: ")
            else:
                break
        except ValueError:
            print("O valor inserido não é um número válido.")
            unidade = input("Digite uma quantidade válida: ")

    while nome.strip() == "":
        print("Campo em branco. Digite novamente.")
        nome = input("Nome: ")

    while descricao.strip() == "":
        print("Campo em branco. Digite novamente.")
        descricao = input("Descrição: ")

    while True:
        try:
            preco = float(preco)
            if preco <= 0:
                print("O valor inserido precisa ser positivo")
                preco = input("Digite um preço válido: ")
            else:
                break
        except ValueError:
            print("O valor inserido não é um número válido.")
            preco = input("Digite um preço válido: ")

    try:
        cursor.execute("INSERT INTO produtos (unidade, nome, descricao, preco) VALUES (?, ?, ?, ?)", (unidade, nome, descricao, preco))
        banco.commit()
        print("Produto adicionado com sucesso!")
    except sqlite3.Error as erro: 
        print("Erro ao adicionar produto:", erro)

def deletar_produto(id_produto, cursor, banco):
    try:
        # Verifica se o produto com o ID fornecido existe
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
        produto = cursor.fetchone()
        if produto:
            cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
            banco.commit()
            print("Produto deletado com sucesso!")
        else:
            print("O produto com o ID", id_produto, "não foi encontrado.")
    except sqlite3.Error as erro:
        print("Erro ao deletar produto:", erro)

def consultar_produto(id_produto, cursor):
    try:
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
        produto = cursor.fetchone()
        if produto:
            print("Produto encontrado:")
            print("ID:", produto[0])
            print("Unidade:", produto[1])
            print("Nome:", produto[2])
            print("Descrição:", produto[3])
            print("Preço:", produto[4])
        else:
            print("Produto não encontrado.")
            opcao = input("Deseja adicionar um novo produto? (S/N): ")
            if opcao.lower() == 's':
                unidade = input("Unidade: ")
                nome = input("Nome do produto: ")
                descricao = input("Descrição do produto: ")
                preco = float(input("Preço do produto: "))
                adicionar_produto(unidade, nome, descricao, preco, cursor, banco)
            else:
                print("Operação cancelada.")
    except sqlite3.Error as erro:
        print("Erro ao consultar produto:", erro)

def atualizar_produto(id_produto, novo_nome, nova_descricao, novo_preco, cursor, banco):
    try:
        # Verifica se o produto com o ID fornecido existe
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
        produto = cursor.fetchone()
        if produto:
            cursor.execute("UPDATE produtos SET nome = ?, descricao = ?, preco = ? WHERE id = ?",
                           (novo_nome, nova_descricao, novo_preco, id_produto))
            banco.commit()
            print("Produto atualizado com sucesso!")
        else:
            print("O produto com o ID", id_produto, "não foi encontrado.")
            opcao = input("Deseja adicionar um novo produto? (S/N): ")
            if opcao.lower() == 's':
                unidade = input("Unidade: ")
                adicionar_produto(id_produto, novo_nome, nova_descricao, novo_preco, cursor, banco)
            else:
                print("Operação cancelada.")
    except sqlite3.Error as erro:
        print("Erro ao atualizar produto:", erro)

def listar_produtos(cursor):
    try:  
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()
        if produtos:
            print("Lista de produtos:")
            for produto in produtos:
                print("ID:", produto[0])
                print("Unidade:", produto[1])
                print("Nome:", produto[2])
                print("Descrição:", produto[3])
                print("Preço:", produto[4])
                print("----------------------")
        else:
            print("Não há produtos cadastrados.")
            opcao = input("Deseja adicionar um novo produto? (S/N): ")
            if opcao.lower() == 's':
                id_produto = input("ID do produto: ")
                unidade = input("Unidade: ")
                nome = input("Nome do produto: ")
                descricao = input("Descrição do produto: ")
                preco = float(input("Preço do produto: "))
                adicionar_produto(id_produto, unidade, nome, descricao, preco, cursor, banco)
            else:
                print("Operação cancelada.")
    except sqlite3.Error as erro:
        print("Erro ao listar produtos:", erro)

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
