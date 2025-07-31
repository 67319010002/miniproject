from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Note, User

notes = Blueprint('notes', __name__)

# 🔹 Get all notes of the current user
@notes.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    all_notes = Note.objects(user=user).order_by('-created_at')
    return jsonify([
        {
            "id": str(note.id),
            "title": note.title,
            "content": note.content,
            "image_url": note.image_url or "",
            "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "username": note.user.username if note.user else "Unknown"
        }
        for note in all_notes
    ])

# 🔹 Create a new note
@notes.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()
    user = User.objects(id=user_id).first()

    note = Note(
        title=data['title'],
        content=data.get('content', ''),
        image_url=data.get('image_url', ''),
        user=user
    )
    note.save()

    return jsonify({"msg": "Note created!"})

# 🔹 Update a note by ID
@notes.route('/notes/<note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    data = request.get_json()
    update_data = {}

    if 'title' in data:
        update_data['title'] = data['title']
    if 'content' in data:
        update_data['content'] = data['content']
    if 'image_url' in data:
        update_data['image_url'] = data['image_url']

    Note.objects(id=note_id).update_one(**update_data)
    return jsonify({"msg": "Note updated!"})

# 🔹 Delete a note by ID
@notes.route('/notes/<note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    Note.objects(id=note_id).delete()
    return jsonify({"msg": "Note deleted!"})

# 🔹 Search user’s own notes
@notes.route('/notes/search', methods=['GET'])
@jwt_required()
def search_notes():
    query = request.args.get('q', '').strip()
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()

    if not query:
        return jsonify({"msg": "Please provide a search query."}), 400

    found_notes = Note.objects(
        user=user,
        __raw__={
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"content": {"$regex": query, "$options": "i"}}
            ]
        }
    ).order_by('-created_at')

    return jsonify([
        {
            "id": str(note.id),
            "title": note.title,
            "content": note.content,
            "image_url": note.image_url or "",
            "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "username": note.user.username if note.user else "Unknown"
        }
        for note in found_notes
    ])

# 🔹 Get all notes of all users
@notes.route('/notes/all', methods=['GET'])
@jwt_required()
def get_all_notes():
    all_notes = Note.objects().order_by('-created_at')
    return jsonify([
        {
            "id": str(note.id),
            "title": note.title,
            "content": note.content,
            "image_url": note.image_url or "",
            "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "username": note.user.username if note.user else "Unknown"
        }
        for note in all_notes
    ])

# 🔹 Search notes across all users
@notes.route('/notes/all/search', methods=['GET'])
@jwt_required()
def search_all_notes():
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify({"msg": "Please provide a search query."}), 400

    found_notes = Note.objects(
        __raw__={
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"content": {"$regex": query, "$options": "i"}}
            ]
        }
    ).order_by('-created_at')

    return jsonify([
        {
            "id": str(note.id),
            "title": note.title,
            "content": note.content,
            "image_url": note.image_url or "",
            "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "username": note.user.username if note.user else "Unknown"
        }
        for note in found_notes
    ])
