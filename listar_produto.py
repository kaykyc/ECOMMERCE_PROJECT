import sqlite3
from adicionar_produto import adicionar_produto
banco = sqlite3.connect('Banco.db')
cursor = banco.cursor()

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