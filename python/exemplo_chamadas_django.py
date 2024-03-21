import requests
import json

def add_item_to_api(title, content, db_host, db_name, db_user, db_password):
    """
    Função para adicionar um item à API Flask.
    """
    item_data = {
        'title': title,
        'content': content,
        'db_host': db_host,
        'db_name': db_name,
        'db_user': db_user,
        'db_password': db_password
    }

    url = 'http://localhost:5000/items'  # Substitua pela URL correta da sua API Flask
    response = requests.post(url, json=item_data)

    if response.status_code == 200:
        return "Item adicionado com sucesso!"
    else:
        return f"Falha ao adicionar o item: {response.text}"

def get_items_from_api(db_host, db_name, db_user, db_password):
    """
    Função para obter a lista de itens da API Flask.
    """
    item_data = {
        'db_host': db_host,
        'db_name': db_name,
        'db_user': db_user,
        'db_password': db_password
    }

    url = 'http://localhost:5000/items-list'  # Substitua pela URL correta da sua API Flask
    response = requests.get(url, json=item_data)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Falha ao obter a lista de itens: {response.text}"

def update_item_in_api(item_id, title, content, db_host, db_name, db_user, db_password):
    """
    Função para atualizar um item na API Flask.
    """
    item_data = {
        'title': title,
        'content': content,
        'db_host': db_host,
        'db_name': db_name,
        'db_user': db_user,
        'db_password': db_password
    }

    url = f'http://localhost:5000/items-update/{item_id}'  # Substitua pela URL correta da sua API Flask
    response = requests.post(url, json=item_data)

    if response.status_code == 200:
        return "Item atualizado com sucesso!"
    else:
        return f"Falha ao atualizar o item: {response.text}"

def delete_item_from_api(item_id, db_host, db_name, db_user, db_password):
    """
    Função para excluir um item da API Flask.
    """
    item_data = {
        'db_host': db_host,
        'db_name': db_name,
        'db_user': db_user,
        'db_password': db_password
    }

    url = f'http://localhost:5000/items-delete/{item_id}'  # Substitua pela URL correta da sua API Flask
    response = requests.delete(url, json=item_data)

    if response.status_code == 200:
        return "Item excluído com sucesso!"
    else:
        return f"Falha ao excluir o item: {response.text}"

# Exemplo de uso das funções
if __name__ == "__main__":
    # Substitua pelos dados do seu item e conexão com o banco de dados
    title = 'Exemplo de Item'
    content = 'Conteúdo do exemplo de item'
    db_host = 'seu_host'
    db_name = 'seu_banco_de_dados'
    db_user = 'seu_usuario'
    db_password = 'sua_senha'

    # Chamada para adicionar um item
    print(add_item_to_api(title, content, db_host, db_name, db_user, db_password))

    # Chamada para obter a lista de itens
    print(get_items_from_api(db_host, db_name, db_user, db_password))

    # Chamada para atualizar um item
    item_id = 1  # Substitua pelo ID do item que deseja atualizar
    new_title = 'Novo título'
    new_content = 'Novo conteúdo'
    print(update_item_in_api(item_id, new_title, new_content, db_host, db_name, db_user, db_password))

    # Chamada para excluir um item
    item_id = 1  # Substitua pelo ID do item que deseja excluir
    print(delete_item_from_api(item_id, db_host, db_name, db_user, db_password))
