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

        completed_progress = (
            UserProgress.query.filter_by(
                completed=True
            ).all()
        )

        completed_subtopic_names = []

        for progress in completed_progress:

            subtopic = SubTopic.query.get(
                progress.subtopic_id
            )

            if subtopic:

                completed_subtopic_names.append(
                    subtopic.name
                )

        completed_subtopics = len(
            completed_subtopic_names
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

            "completed_subtopic_names":
                completed_subtopic_names,

            "progress_percentage":
                percentage
        }