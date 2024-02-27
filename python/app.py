from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']# Configurar a URI do banco de dados

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run()

#Model
class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(255))

    def __init__(self, title, content):
        self.title = title
        self.content = content

with app.app_context():
    db.create_all()  # Criar tabelas apenas quando o script é executado diretamente

@app.route('/', methods=['GET'])
def get():
    return "Hello World"

@app.route('/items', methods=['POST'])
def itemadd():
    body = request.get_json()

    title = body['title']
    content = body['content']

    db.session.add(Items(title, content))
    db.session.commit()

    return "item"

@app.route('/items-list', methods=['GET'])
def item_list():
    items = Items.query.all()

    # Convertendo os itens para um formato serializável (por exemplo, JSON)
    items_list = []
    for item in items:
        items_list.append({
            'id': item.id,
            'title': item.title,
            'content': item.content
        })

    return jsonify(items_list)

@app.route('/items-update/<int:item_id>', methods=['POST'])
def item_update(item_id):
    try:
        # Obtém o item específico pelo ID
        item = Items.query.get(item_id)

        if not item:
            return jsonify({'error': 'Item não encontrado'}), 404

        # Atualiza os dados do item com base no JSON fornecido
        body = request.get_json()
        item.title = body.get('title', item.title)
        item.content = body.get('content', item.content)

        # Commit para salvar as alterações no banco de dados
        db.session.commit()

        return jsonify({'message': 'Item atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/items-delete/<int:item_id>', methods=['DELETE'])
def item_delete(item_id):
    try:
        # Busca o item pelo ID
        item = Items.query.get(item_id)

        if not item:
            return jsonify({'error': 'Item não encontrado'}), 404

        # Remove o item do banco de dados
        db.session.delete(item)
        db.session.commit()

        return jsonify({'message': 'Item excluído com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500