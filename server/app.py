from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Extensions
CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

# ROUTES

# GET all messages
@app.route('/messages', methods=['GET'])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([
        {
            "id": m.id,
            "body": m.body,
            "username": m.username,
            "created_at": m.created_at.isoformat() if m.created_at else None,
            "updated_at": m.updated_at.isoformat() if m.updated_at else None
        }
        for m in messages
    ]), 200

# POST new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    body = data.get("body")
    username = data.get("username")

    if not body or not username:
        return jsonify({"error": "Missing 'body' or 'username'"}), 400

    new_message = Message(body=body, username=username)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({
        "id": new_message.id,
        "body": new_message.body,
        "username": new_message.username,
        "created_at": new_message.created_at.isoformat() if new_message.created_at else None,
        "updated_at": new_message.updated_at.isoformat() if new_message.updated_at else None
    }), 201

# PATCH message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({"error": "Message not found"}), 404

    data = request.get_json()
    new_body = data.get("body")

    if new_body:
        message.body = new_body
        db.session.commit()

    return jsonify({
        "id": message.id,
        "body": message.body,
        "username": message.username,
        "created_at": message.created_at.isoformat() if message.created_at else None,
        "updated_at": message.updated_at.isoformat() if message.updated_at else None
    }), 200

# DELETE message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({"error": "Message not found"}), 404

    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": "Message deleted"}), 200

# Placeholder GET by id
@app.route('/messages/<int:id>', methods=['GET'])
def messages_by_id(id):
    return jsonify({"message": "This route is not implemented yet."}), 200

# Run the app
if __name__ == '__main__':
    app.run(port=5555)
