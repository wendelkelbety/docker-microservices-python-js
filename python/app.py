from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure the database URI with a default value
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'postgresql+psycopg2://postgres:ra04ra@db:5432/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy instance
db = SQLAlchemy(app)

# Model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(255))

    def __init__(self, title, content):
        self.title = title
        self.content = content

# Create tables only when the script is executed directly
if __name__ == '__main__':
    db.create_all()

# Routes
@app.route('/', methods=['GET'])
def hello_world():
    return "Hello World"

@app.route('/items', methods=['POST'])
def add_item():
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return jsonify({"error": "Title and content are required"}), 400

        new_item = Item(title=title, content=content)

        db.session.add(new_item)
        db.session.commit()

        return jsonify({"message": "Item added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the application
    app.run(debug=True)
