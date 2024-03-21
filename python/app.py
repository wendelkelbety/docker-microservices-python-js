from flask import Flask, request, jsonify
import pyodbc
import os

app = Flask(__name__)

def establish_connection(connection_string):
    # Função para estabelecer a conexão com o banco de dados
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    return connection, cursor

@app.route('/', methods=['GET'])
def get():
    return "Hello World"

@app.route('/items', methods=['POST'])
def itemadd():
    body = request.get_json()

    # Obter os dados de conexão do corpo da solicitação JSON
    db_host = body.get('db_host')
    db_name = body.get('db_name')
    db_user = body.get('db_user')
    db_password = body.get('db_password')

    # Construir a string de conexão com base nos dados fornecidos
    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_host};DATABASE={db_name};UID={db_user};PWD={db_password};"

    # Estabelecer a conexão com o banco de dados
    connection, cursor = establish_connection(connection_string)

    # Extrair os dados do item do corpo da solicitação JSON
    title = body['title']
    content = body['content']

    # Executar a inserção no banco de dados usando pyodbc
    cursor.execute("INSERT INTO Items (title, content) VALUES (?, ?)", title, content)
    connection.commit()

    # Fechar a conexão após a conclusão da operação
    connection.close()

    return "item"

@app.route('/items-list', methods=['GET'])
def item_list():
    body = request.get_json()

    # Obter os dados de conexão do corpo da solicitação JSON
    db_host = body.get('db_host')
    db_name = body.get('db_name')
    db_user = body.get('db_user')
    db_password = body.get('db_password')

    # Construir a string de conexão com base nos dados fornecidos
    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_host};DATABASE={db_name};UID={db_user};PWD={db_password};"

    # Estabelecer a conexão com o banco de dados
    connection, cursor = establish_connection(connection_string)

    # Executar a consulta no banco de dados usando pyodbc
    cursor.execute("SELECT * FROM Items")
    items = cursor.fetchall()

    # Converter os itens para um formato serializável (por exemplo, JSON)
    items_list = []
    for item in items:
        items_list.append({
            'id': item.id,
            'title': item.title,
            'content': item.content
        })

    # Fechar a conexão após a conclusão da operação
    connection.close()

    return jsonify(items_list)

@app.route('/items-update/<int:item_id>', methods=['POST'])
def item_update(item_id):
    body = request.get_json()

    # Obter os dados de conexão do corpo da solicitação JSON
    db_host = body.get('db_host')
    db_name = body.get('db_name')
    db_user = body.get('db_user')
    db_password = body.get('db_password')

    # Construir a string de conexão com base nos dados fornecidos
    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_host};DATABASE={db_name};UID={db_user};PWD={db_password};"

    # Estabelecer a conexão com o banco de dados
    connection, cursor = establish_connection(connection_string)

    try:
        # Obtém o item específico pelo ID
        cursor.execute("SELECT * FROM Items WHERE id = ?", item_id)
        item = cursor.fetchone()

        if not item:
            return jsonify({'error': 'Item não encontrado'}), 404

        # Atualiza os dados do item com base no JSON fornecido
        title = body.get('title')
        content = body.get('content')

        cursor.execute("UPDATE Items SET title = ?, content = ? WHERE id = ?", title, content, item_id)
        connection.commit()

        return jsonify({'message': 'Item atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Fechar a conexão após a conclusão da operação
        connection.close()
    
@app.route('/items-delete/<int:item_id>', methods=['DELETE'])
def item_delete(item_id):
    # Obter os dados de conexão do corpo da solicitação JSON
    body = request.get_json()
    db_host = body.get('db_host')
    db_name = body.get('db_name')
    db_user = body.get('db_user')
    db_password = body.get('db_password')

    # Construir a string de conexão com base nos dados fornecidos
    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_host};DATABASE={db_name};UID={db_user};PWD={db_password};"

    # Estabelecer a conexão com o banco de dados
    connection, cursor = establish_connection(connection_string)

    try:
        # Busca o item pelo ID
        cursor.execute("SELECT * FROM Items WHERE id = ?", item_id)
        item = cursor.fetchone()

        if not item:
            return jsonify({'error': 'Item não encontrado'}), 404

        # Remove o item do banco de dados
        cursor.execute("DELETE FROM Items WHERE id = ?", item_id)
        connection.commit()

        return jsonify({'message': 'Item excluído com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Fechar a conexão após a conclusão da operação
        connection.close()

if __name__ == '__main__':
    app.run()
