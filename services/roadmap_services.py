from models import Career, Topic
from database import db
from services.ai_service import (
    AIService
)


class RoadmapService:

    @staticmethod
    def generate_mock_topics(career_name):
        """
        Temporary roadmap generator.
        Gemini/OpenAI will replace this later.
        """

        mock_roadmaps = {
            "Data Scientist": [
                "Python",
                "Statistics",
                "Machine Learning",
                "Deep Learning",
                "Data Visualization"
            ],

            "AI Engineer": [
                "Python",
                "Machine Learning",
                "Deep Learning",
                "LLMs",
                "MLOps"
            ],

            "Frontend Developer": [
                "HTML",
                "CSS",
                "JavaScript",
                "React",
                "Next.js"
            ]
        }

        return mock_roadmaps.get(
            career_name,
            [
                "Fundamentals",
                "Intermediate Concepts",
                "Projects",
                "Advanced Concepts"
            ]
        )

    @staticmethod
    def get_or_create_roadmap(career_name):

        career = Career.query.filter_by(
            name=career_name
        ).first()

        # Career already exists
        if career:

            topics = [
                topic.name
                for topic in career.topics
            ]

            return {
                "career": career.name,
                "topics": topics,
                "source": "database"
            }

        # Career does not exist
        career = Career(
            name=career_name
        )

        db.session.add(career)
        db.session.commit()

        generated_topics = (
            AIService.generate_roadmap_topics(
                career_name
            )
        )

        for topic_name in generated_topics:

            topic = Topic(
                name=topic_name,
                career_id=career.id
            )

            db.session.add(topic)

        db.session.commit()

        return {
            "career": career.name,
            "topics": generated_topics,
            "source": "generated"
        }