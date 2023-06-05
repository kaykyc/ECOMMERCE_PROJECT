import sqlite3

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