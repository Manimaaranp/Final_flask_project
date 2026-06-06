from database import db
"""Database models for the Career Roadmap Generator."""


class Career(db.Model):
    __tablename__ = "careers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    topics = db.relationship(
        "Topic",
        backref="career",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Topic(db.Model):
    __tablename__ = "topics"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    career_id = db.Column(
        db.Integer,
        db.ForeignKey("careers.id"),
        nullable=False
    )

    subtopics = db.relationship(
        "SubTopic",
        backref="topic",
        lazy=True,
        cascade="all, delete-orphan"
    )


class SubTopic(db.Model):
    __tablename__ = "subtopics"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    topic_id = db.Column(
        db.Integer,
        db.ForeignKey("topics.id"),
        nullable=False
    )

    contents = db.relationship(
        "LearningContent",
        backref="subtopic",
        lazy=True,
        cascade="all, delete-orphan"
    )

    quizzes = db.relationship(
        "Quiz",
        backref="subtopic",
        lazy=True,
        cascade="all, delete-orphan"
    )

    progress_records = db.relationship(
        "UserProgress",
        backref="subtopic",
        lazy=True,
        cascade="all, delete-orphan"
    )


class LearningContent(db.Model):
    __tablename__ = "learning_contents"

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.Text, nullable=False)

    subtopic_id = db.Column(
        db.Integer,
        db.ForeignKey("subtopics.id"),
        nullable=False
    )


class Quiz(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    question = db.Column(
        db.Text,
        nullable=False
    )

    option_a = db.Column(
        db.Text,
        nullable=False
    )

    option_b = db.Column(
        db.Text,
        nullable=False
    )

    option_c = db.Column(
        db.Text,
        nullable=False
    )

    option_d = db.Column(
        db.Text,
        nullable=False
    )

    correct_answer = db.Column(
        db.String(1),
        nullable=False
    )

    subtopic_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "subtopics.id"
        ),
        nullable=False
    )

    attempts = db.relationship(
        "QuizAttempt",
        backref="quiz",
        lazy=True,
        cascade="all, delete-orphan"
    )


class QuizAttempt(db.Model):
    __tablename__ = "quiz_attempts"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "quizzes.id"
        ),
        nullable=False
    )

    answered_correctly = db.Column(
        db.Boolean,
        default=False
    )


class UserProgress(db.Model):
    __tablename__ = "user_progress"

    id = db.Column(db.Integer, primary_key=True)

    completed = db.Column(
        db.Boolean,
        default=False
    )

    subtopic_id = db.Column(
        db.Integer,
        db.ForeignKey("subtopics.id"),
        nullable=False
    )