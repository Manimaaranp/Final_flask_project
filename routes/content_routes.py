from flask import (
    Blueprint,
    request,
    jsonify
)

from services.content_service import (
    ContentService
)

content_bp = Blueprint(
    "content",
    __name__
)


@content_bp.route(
    "/generate-content",
    methods=["POST"]
)
def generate_content():

    data = request.get_json()

    subtopic_name = data.get(
        "subtopic_name"
    )

    if not subtopic_name:

        return jsonify({
            "error":
            "subtopic_name is required"
        }), 400

    result = (
        ContentService
        .get_or_create_content(
            subtopic_name
        )
    )

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200