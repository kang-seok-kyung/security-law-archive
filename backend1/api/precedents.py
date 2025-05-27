from flask import Blueprint, request, jsonify
from db import db
from config import COLLECTION_NAME

bp = Blueprint("precedents", __name__, url_prefix="/api/precedents")
collection = db[COLLECTION_NAME]

@bp.route("", methods=["POST"])
def insert_precedent():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    inserted = collection.insert_one(data)
    return jsonify({"message": "Inserted", "id": str(inserted.inserted_id)}), 201
