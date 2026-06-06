from flask import Flask

from database import db
from routes.roadmap_routes import roadmap_bp
from routes.subtopic_routes import subtopic_bp
from routes.content_routes import (
    content_bp
)
from routes.quiz_routes import quiz_bp
from routes.progress_routes import progress_bp

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///roadmap.db"

app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(
    roadmap_bp,
    url_prefix="/api"
)
app.register_blueprint(
    subtopic_bp,
    url_prefix="/api"
)
app.register_blueprint(
    content_bp,
    url_prefix="/api"
)
app.register_blueprint(
    quiz_bp,
    url_prefix="/api"
)

app.register_blueprint(
    progress_bp,
    url_prefix="/api"
)
if __name__ == "__main__":
    app.run(debug=True)