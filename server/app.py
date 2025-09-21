from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)
CORS(app)


@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([m.to_dict() for m in messages])


@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201


@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)   # ✅ FIXED
    if not message:
        return {"error": "Message not found"}, 404

    data = request.get_json()
    if "body" in data:
        message.body = data["body"]
    db.session.commit()

    return jsonify(message.to_dict()), 200


@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)   # ✅ FIXED
    if not message:
        return {"error": "Message not found"}, 404

    db.session.delete(message)
    db.session.commit()

    return {}, 204


# Optional root route so flask run doesn't show 404
@app.route('/')
def home():
    return {"message": "Chatterbox API is running 🎉"}
