# Career Roadmap Generator

## Overview

AI Learning Roadmap Generator is a Flask-based web application that generates personalized learning roadmaps using Google's Gemini AI. Users can select a career path, explore relevant topics and subtopics, access AI-generated learning content, complete quizzes, and track their learning progress.The application provides an end-to-end learning experience by combining AI-generated educational content with progress tracking and assessment features.


## Features

### Roadmap Generation

* Generate career-specific learning roadmaps using Gemini AI.
* Topics are generated in a structured learning sequence.

### Subtopic Generation

* Generate topic-specific subtopics.
* Subtopics are arranged from beginner to advanced level.

### Learning Content Generation

* Generate detailed educational content for each subtopic.
* Content is created dynamically using Gemini AI.

### Quiz Generation

* Generate multiple-choice quizzes from learning content.
* Questions are based on generated educational material.

### Quiz Verification

* Verify user answers.
* Track quiz completion.

### Progress Tracking

* Monitor completed subtopics.
* Display overall learning progress.
* Highlight completed subtopics visually.

### Database Integration

* Stores:

  * Careers
  * Topics
  * Subtopics
  * Learning Content
  * Quizzes
  * Quiz Attempts
  * User Progress


## Technology Stack

### Backend

* Python
* Flask
* Python-dotenv
* SQLAlchemy
* SQLite
* Google Gemini AI

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap 5

### Version Control

* Git
* GitHub


## Project Structure

```text
project-root/
│
├── app.py
├── database.py
├── models.py
├── requirements.txt
│
├── routes/
│   ├── roadmap_routes.py
│   ├── subtopic_routes.py
│   ├── content_routes.py
│   ├── quiz_routes.py
│   ├── progress_routes.py
│   └── pages_routes.py
│
├── services/
│   ├── ai_service.py
│   ├── roadmap_service.py
│   ├── subtopic_service.py
│   ├── content_service.py
│   ├── quiz_service.py
│   └── progress_service.py
│
├── templates/
│
├── static/
│   ├── css/
│   └── js/
│
└── instance/
    └── roadmap.db
```
## Live Demo

Application URL:

https://your-render-url.onrender.com


## Installation

### Clone Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```


## Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```


## Running the Application

```bash
python app.py
```

Application will run on:

```text
http://127.0.0.1:5000
```


## Workflow

```text
Career Selection
        ↓
Roadmap Generation
        ↓
Topic Selection
        ↓
Subtopic Generation
        ↓
Learning Content
        ↓
Quiz Generation
        ↓
Quiz Verification
        ↓
Progress Tracking
```


## Future Enhancements

* User Authentication
* Multi-user Support
* Personalized Learning Recommendations
* Dashboard Analytics
* AI Chat Tutor
* Cloud Database Integration
* Docker Deployment


## Authors

Manimaaran Pugaleswaran, Aswin Puthanpura Sachidhanandhan

Master's in Applied Data Science and Artificial Intelligence

SRH University, Hamburg
