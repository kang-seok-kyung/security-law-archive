from flask import Blueprint, request, jsonify
from services.precedent_service import find_by_laws, find_by_id

bp = Blueprint("precedents", __name__, url_prefix="/api/precedents")

@bp.route("", methods=["GET"])
def get_precedents_by_law():
    laws = request.args.getlist("law")
    if not laws:
        return jsonify({"error": "law 파라미터가 필요합니다."}), 400
    results = find_by_laws(laws)
    return jsonify(results)

@bp.route("/<precedent_id>", methods=["GET"])
def get_precedent_detail(precedent_id):
    result = find_by_id(precedent_id)
    if not result:
        return jsonify({"error": "판례를 찾을 수 없습니다."}), 404
    return jsonify(result)