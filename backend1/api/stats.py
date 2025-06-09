from flask import Blueprint, jsonify
from services.stat_service import count_cases_by_law, count_precedents_by_year, count_precedents_by_law

bp = Blueprint("stats", __name__, url_prefix="/api/stats")

@bp.route("/precedents/by-year", methods=["GET"])
def get_precedent_by_year():
    stats = count_precedents_by_year()
    return jsonify(stats)

@bp.route("/precedents/by-law", methods=["GET"])
def get_precedent_by_law():
    stats = count_precedents_by_law()
    return jsonify(stats)

@bp.route("/cases/by-law", methods=["GET"])
def get_cases_by_law():
    stats = count_cases_by_law()
    return jsonify(stats)