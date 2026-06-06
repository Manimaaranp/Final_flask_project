from database import db
from models import (
    Quiz,
    SubTopic,
    LearningContent,
    QuizAttempt,
    UserProgress,
    SubTopic
)
from services.ai_service import (
    AIService
)
from services.progress_service import (
    ProgressService
)


class QuizService:

    @staticmethod
    def generate_mock_quiz(
        subtopic_name
    ):

        mock_quizzes = {

            "Variables": [
                {
                    "question": "What is a variable?",
                    "answer": "A container used to store data"
                },
                {
                    "question": "Which symbol is used for assignment in Python?",
                    "answer": "="
                }
            ],

            "Loops": [
                {
                    "question": "Which loop repeats a fixed number of times?",
                    "answer": "for loop"
                },
                {
                    "question": "Which loop continues while a condition is true?",
                    "answer": "while loop"
                }
            ],

            "Functions": [
                {
                    "question": "Which keyword defines a function?",
                    "answer": "def"
                },
                {
                    "question": "Why are functions used?",
                    "answer": "Code reusability"
                }
            ]
        }

        return mock_quizzes.get(
            subtopic_name,
            [
                {
                    "question": f"What is {subtopic_name}?",
                    "answer": "Sample Answer"
                }
            ]
        )

    @staticmethod
    def get_or_create_quiz(
        subtopic_name
    ):

        subtopic = SubTopic.query.filter_by(
            name=subtopic_name
        ).first()

        if not subtopic:
            return {
                "error": "Subtopic not found"
            }
        learning_content = LearningContent.query.filter_by(
            subtopic_id=subtopic.id
        ).first()
        if not learning_content:
          return {
              "error": "Learning content not found"
          }
        content = learning_content.content

        existing_quizzes = Quiz.query.filter_by(
            subtopic_id=subtopic.id
        ).all()

        if existing_quizzes:

            return {
                "subtopic": subtopic.name,
                "quiz": [
                    {
                        "id": q.id,
                        "question": q.question,
                        "option_a": q.option_a,
                        "option_b": q.option_b,
                        "option_c": q.option_c,
                        "option_d": q.option_d
                    }
                    for q in existing_quizzes
                ],
                "source": "database"
            }

        generated_quiz = (
            AIService.generate_quiz(
                subtopic_name,
                content
            )
        )

        for item in generated_quiz:

            quiz = Quiz(
                question=item["question"],
                option_a=item["option_a"],
                option_b=item["option_b"],
                option_c=item["option_c"],
                option_d=item["option_d"],
                correct_answer=item["correct_answer"],
                subtopic_id=subtopic.id
            )

            db.session.add(quiz)

        db.session.commit()

        return {
            "subtopic": subtopic.name,
            "quiz": [
                {
                    "question": q["question"],
                    "option_a": q["option_a"],
                    "option_b": q["option_b"],
                    "option_c": q["option_c"],
                    "option_d": q["option_d"]
                }
                for q in generated_quiz
            ],
            "source": "generated"
        }
    @staticmethod
    def verify_quiz_answer(
        quiz_id,
        selected_answer
    ):

        quiz = Quiz.query.get(
            quiz_id
        )

        if not quiz:
            return {
                "error": "Quiz not found"
            }

        is_correct = (
            selected_answer.upper()
            ==
            quiz.correct_answer.upper()
        )

        attempt = QuizAttempt(
            quiz_id=quiz.id,
            answered_correctly=is_correct
        )

        db.session.add(attempt)
        db.session.commit()

        if not is_correct:

            return {
                "correct": False,
                "message":
                "Incorrect. Try again.",
                "correct_answer":
                quiz.correct_answer
            }

        subtopic = SubTopic.query.get(
            quiz.subtopic_id
        )

        all_quizzes = Quiz.query.filter_by(
            subtopic_id=subtopic.id
        ).all()

        all_correct = True

        for subtopic_quiz in all_quizzes:

            correct_attempt = (
                QuizAttempt.query.filter_by(
                    quiz_id=subtopic_quiz.id,
                    answered_correctly=True
                ).first()
            )

            if not correct_attempt:
                all_correct = False
                break

        if all_correct:

            ProgressService.update_progress(
                subtopic.name,
                True
            )

        return {
            "correct": True,
            "message": "Correct!"
        }