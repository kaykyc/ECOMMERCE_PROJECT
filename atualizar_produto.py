import sqlite3
from adicionar_produto import adicionar_produto

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