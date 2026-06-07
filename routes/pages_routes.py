from flask import (
    Blueprint,
    render_template
)

page_bp = Blueprint(
    "pages",
    __name__
)


@page_bp.route("/")
def home():
    return render_template(
        "index.html"
    )


@page_bp.route("/roadmap")
def roadmap():
    return render_template(
        "roadmap.html"
    )


@page_bp.route("/topic")
def topic():
    return render_template(
        "topic.html"
    )
   

@page_bp.route("/subtopic")
def subtopic():
    return render_template(
        "subtopic.html"
    )


@page_bp.route("/content")
def content():
    return render_template(
        "content.html"
    )


@page_bp.route("/quiz")
def quiz():
    return render_template(
        "quiz.html"
    )


@page_bp.route("/progress")
def progress():
    return render_template(
        "progress.html"
    )


@page_bp.route("/login")
def login():
    return render_template(
        "login.html"
    )


@page_bp.route("/signup")
def signup():
    return render_template(
        "signup.html"
    )