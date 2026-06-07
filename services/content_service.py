from database import db
from models import (
    SubTopic,
    LearningContent
)
from services.ai_service import (
    AIService
)


class ContentService:

    @staticmethod
    def get_or_create_content(
        subtopic_name
    ):

        subtopic = SubTopic.query.filter_by(
            name=subtopic_name
        ).first()

        if not subtopic:
            return {
                "error": "Subtopic not found"
            }

        existing_content = (
            LearningContent.query.filter_by(
                subtopic_id=subtopic.id
            ).first()
        )

        if existing_content:

            return {
                "subtopic": subtopic.name,
                "content": existing_content.content,
                "source": "database"
            }

        generated_content = (
            AIService.generate_learning_content(
                subtopic_name
            )
        )

        content = LearningContent(
            content=generated_content,
            subtopic_id=subtopic.id
        )

        db.session.add(content)
        db.session.commit()

        return {
            "subtopic": subtopic.name,
            "content": generated_content,
            "source": "generated"
        }