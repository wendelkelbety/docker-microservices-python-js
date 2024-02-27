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