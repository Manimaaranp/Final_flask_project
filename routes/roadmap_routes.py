from flask import Blueprint, request, jsonify

from services.roadmap_services import RoadmapService

roadmap_bp = Blueprint(
    "roadmap",
    __name__
)


@roadmap_bp.route(
    "/generate-roadmap",
    methods=["POST"]
)
def generate_roadmap():

    data = request.get_json()

    career_name = data.get(
        "career_name"
    )

    if not career_name:

        return jsonify({
            "error": "career_name is required"
        }), 400

    roadmap = (
        RoadmapService
        .get_or_create_roadmap(career_name)
    )

    return jsonify(roadmap), 200