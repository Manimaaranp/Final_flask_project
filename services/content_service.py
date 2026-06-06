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
    def generate_mock_content(
        subtopic_name
    ):

        mock_contents = {

            "Variables": """
Variables are used to store data in memory.

Example:

x = 10
name = "John"

Variables allow programs to reuse and manipulate values throughout execution.
            """,

            "Loops": """
Loops allow repeated execution of code.

Python supports:

1. for loop
2. while loop

Example:

for i in range(5):
    print(i)
            """,

            "Functions": """
Functions are reusable blocks of code.

Example:

def greet():
    print("Hello")

Functions improve code reusability and readability.
            """,

            "Object-Oriented Programming": """
Object-Oriented Programming (OOP) organizes code using classes and objects.

Core concepts:

1. Encapsulation
2. Inheritance
3. Polymorphism
4. Abstraction
            """,

            "Pandas": """
Pandas is a Python library used for data analysis.

Common operations:

- Reading CSV files
- Filtering data
- Aggregation
- Data cleaning
            """
        }

        return mock_contents.get(
            subtopic_name,
            f"""
Introduction to {subtopic_name}

This is sample learning content generated for testing purposes.

Detailed AI-generated content will be added in future phases.
            """
        )

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