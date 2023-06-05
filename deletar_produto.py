import sqlite3

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

