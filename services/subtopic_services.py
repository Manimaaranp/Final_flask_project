from database import db
from models import Topic, SubTopic
from services.ai_service import (
    AIService
)


class SubTopicService:

    @staticmethod
    def get_or_create_subtopics(topic_name):

        topic = Topic.query.filter_by(
            name=topic_name
        ).first()
        

        if not topic:
            return {
                "error": "Topic not found"
            }
        
        career_name = topic.career.name
        existing_subtopics = SubTopic.query.filter_by(
            topic_id=topic.id
        ).all()

        if existing_subtopics:

            return {
                "topic": topic.name,
                "subtopics": [
                    subtopic.name
                    for subtopic in existing_subtopics
                ],
                "source": "database"
            }

        generated_subtopics = (
            AIService.generate_subtopics(
                topic_name,
                career_name
            )
        )

        for subtopic_name in generated_subtopics:

            subtopic = SubTopic(
                name=subtopic_name,
                topic_id=topic.id
            )

            db.session.add(subtopic)

        db.session.commit()

        return {
            "topic": topic.name,
            "subtopics": generated_subtopics,
            "source": "generated"
        }