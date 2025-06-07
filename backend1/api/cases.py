from flask import Blueprint, jsonify
from db import db
from config import COLLECTION_NAME2, COLLECTION_NAME1
from bson import ObjectId

bp = Blueprint("cases", __name__, url_prefix="/api/cases")

cases_col = db[COLLECTION_NAME2]
precedents_col = db[COLLECTION_NAME1]

@bp.route("", methods=["GET"])
def get_all_cases(): 
    results = list(cases_col.find({}, {"_id": 1, "title": 1, "date": 1}))
    for r in results:
        r["_id"] = str(r["_id"])
    return jsonify(results)

@bp.route("/<case_id>", methods=["GET"])
def get_case_detail(case_id):
    case = cases_col.find_one({"_id": ObjectId(case_id)})
    if not case:
        return jsonify({"error": "사건을 찾을 수 없습니다."}), 404

    laws = case.get("related_laws", [])
    if isinstance(laws, str):
        laws = [laws]
    precedents = list(precedents_col.find({"jo": {"$in": laws}}, {"_id": 0, "id": 1, "title": 1, "court": 1, "date": 1, "url": 1}))

    case["_id"] = str(case["_id"])
    return jsonify({"case": case, "related_precedents": precedents})