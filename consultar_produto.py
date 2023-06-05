import sqlite3
from adicionar_produto import adicionar_produto
banco = sqlite3.connect('Banco.db')
cursor = banco.cursor()

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