from flask import (
    Blueprint,
    request,
    jsonify
)

from services.quiz_service import (
    QuizService
)

quiz_bp = Blueprint(
    "quiz",
    __name__
)


@quiz_bp.route(
    "/generate-quiz",
    methods=["POST"]
)
def generate_quiz():

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
        QuizService.get_or_create_quiz(
            subtopic_name
        )
    )

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200

@quiz_bp.route(
    "/submit-quiz",
    methods=["POST"]
)
def submit_quiz():

    data = request.get_json()

    quiz_id = data.get(
        "quiz_id"
    )

    selected_answer = data.get(
        "selected_answer"
    )

    if not quiz_id:
        return jsonify({
            "error": "quiz_id is required"
        }), 400

    if not selected_answer:
        return jsonify({
            "error":
            "selected_answer is required"
        }), 400

    result = QuizService.verify_quiz_answer(
        quiz_id,
        selected_answer
    )

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200