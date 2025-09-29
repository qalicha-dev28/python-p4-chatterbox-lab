# server/app.py
from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

migrate = Migrate(app, db)
db.init_app(app)

CORS(app)
api = Api(app)

class Messages(Resource):
    def get(self):
        messages = Message.query.order_by(Message.created_at.asc()).all()
        messages_dict = [message.to_dict() for message in messages]
        return make_response(jsonify(messages_dict), 200)

    def post(self):
        data = request.get_json()
        
        try:
            new_message = Message(
                body=data['body'],
                username=data['username']
            )
            
            db.session.add(new_message)
            db.session.commit()
            
            return make_response(jsonify(new_message.to_dict()), 201)
            
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 400)

api.add_resource(Messages, '/messages')

class MessageByID(Resource):
    def get(self, id):
        message = Message.query.filter_by(id=id).first()
        
        if not message:
            return make_response(jsonify({"error": "Message not found"}), 404)
            
        return make_response(jsonify(message.to_dict()), 200)

    def patch(self, id):
        message = Message.query.filter_by(id=id).first()
        
        if not message:
            return make_response(jsonify({"error": "Message not found"}), 404)
        
        data = request.get_json()
        
        if 'body' in data:
            message.body = data['body']
        
        db.session.commit()
        
        return make_response(jsonify(message.to_dict()), 200)

    def delete(self, id):
        message = Message.query.filter_by(id=id).first()
        
        if not message:
            return make_response(jsonify({"error": "Message not found"}), 404)
        
        db.session.delete(message)
        db.session.commit()
        
        return make_response('', 204)

api.add_resource(MessageByID, '/messages/<int:id>')

@app.route('/')
def index():
    return '<h1>Chatterbox API</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)