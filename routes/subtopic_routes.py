from flask import Blueprint, request, jsonify

from services.subtopic_services import (
    SubTopicService
)

subtopic_bp = Blueprint(
    "subtopic",
    __name__
)


@subtopic_bp.route(
    "/generate-subtopics",
    methods=["POST"]
)
def generate_subtopics():

    data = request.get_json()

    topic_name = data.get(
        "topic_name"
    )

    if not topic_name:

        return jsonify({
            "error": "topic_name is required"
        }), 400

    result = (
        SubTopicService
        .get_or_create_subtopics(
            topic_name
        )
    )

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200