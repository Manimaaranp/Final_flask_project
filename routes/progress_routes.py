from flask import (
    Blueprint,
    request,
    jsonify
)

from services.progress_service import (
    ProgressService
)

progress_bp = Blueprint(
    "progress",
    __name__
)


@progress_bp.route(
    "/progress",
    methods=["POST"]
)
def update_progress():

    data = request.get_json()

    subtopic_name = data.get(
        "subtopic_name"
    )

    completed = data.get(
        "completed"
    )

    if subtopic_name is None:
        return jsonify({
            "error":
            "subtopic_name is required"
        }), 400

    result = (
        ProgressService.update_progress(
            subtopic_name,
            completed
        )
    )

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200


@progress_bp.route(
    "/progress",
    methods=["GET"]
)
def get_progress():

    result = (
        ProgressService
        .get_progress_summary()
    )

    return jsonify(result), 200