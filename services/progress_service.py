from database import db
from models import (
    UserProgress,
    SubTopic
)


class ProgressService:

    @staticmethod
    def update_progress(
        subtopic_name,
        completed
    ):

        subtopic = SubTopic.query.filter_by(
            name=subtopic_name
        ).first()

        if not subtopic:
            return {
                "error": "Subtopic not found"
            }

        progress = UserProgress.query.filter_by(
            subtopic_id=subtopic.id
        ).first()

        if progress:

            progress.completed = completed

        else:

            progress = UserProgress(
                completed=completed,
                subtopic_id=subtopic.id
            )

            db.session.add(progress)

        db.session.commit()

        return {
            "subtopic": subtopic_name,
            "completed": completed
        }

    @staticmethod
    def get_progress_summary():

        total_subtopics = (
            SubTopic.query.count()
        )

        completed_subtopics = (
            UserProgress.query.filter_by(
                completed=True
            ).count()
        )

        percentage = 0

        if total_subtopics > 0:

            percentage = round(
                (
                    completed_subtopics /
                    total_subtopics
                ) * 100,
                2
            )

        return {
            "total_subtopics":
                total_subtopics,

            "completed_subtopics":
                completed_subtopics,

            "progress_percentage":
                percentage
        }