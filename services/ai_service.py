import os

from dotenv import load_dotenv

import google.generativeai as genai


load_dotenv()


class AIService:

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    genai.configure(
        api_key=api_key
    )

    model = genai.GenerativeModel(
        "gemini-flash-latest"
    )

    @classmethod
    def generate_text(
        cls,
        prompt
    ):

        response = cls.model.generate_content(
            prompt
        )

        return response.text.strip()
    @classmethod
    def generate_roadmap_topics(
      cls,
      career_name
    ):

      prompt = f"""
        Generate a learning roadmap for becoming a {career_name}.

        IMPORTANT:
        Return exactly 10 topics.

        Output format example:

        Python
        Statistics
        Machine Learning
        Deep Learning
        MLOps

        Rules:
        - One topic per line.
        - No numbering.
        - No bullets.
        - No commas.
        - No explanations.
        - No introductory text.
        - Return only the 10 topic names.
        """
      response = cls.generate_text(
          prompt
      )

      topics = [
          topic.strip()
          for topic in response.split("\n")
          if topic.strip()
      ]

      return topics
    
    @classmethod
    def generate_subtopics(
        cls,
        topic_name,
        career_name
    ):

        prompt = f"""
    You are an expert curriculum designer.

    Career:
    {career_name}

    Topic:
    {topic_name}

    Generate exactly 10 subtopics.

    IMPORTANT:

    The subtopics must be useful for the career "{career_name}".

    Do NOT generate generic academic subtopics.

    Only include concepts that would realistically be learned by a {career_name}.

    Requirements:
    IMPORTANT:

      Assume the learner is a complete beginner.

      The first 5 subtopics must cover fundamentals.

      Avoid advanced concepts unless they naturally come after the fundamentals.

      Do not include highly specialized topics such as:
      - Eigenvalues
      - Entropy
      - Maximum Likelihood Estimation
      - PCA

      unless they are required at the end of the learning path.
    - Return exactly 10 subtopics.
    - Arrange from beginner to advanced.
    - Each subtopic should build upon the previous one.
    - Keep each subtopic short.
    - One subtopic per line.
    - Focus on practical industry relevance.

    Rules:
    - No numbering.
    - No bullets.
    - No explanations.
    - No blank lines.
    - No commas.
    - Return only the subtopic names.

    Example:

    If Career = Data Scientist
    and Topic = Statistics

    Good Output:
    Probability
    Descriptive Statistics
    Inferential Statistics
    Distributions
    Hypothesis Testing
    Sampling Techniques
    Feature Engineering Statistics
    Regression Statistics
    A/B Testing
    Statistical Modeling

    Bad Output:
    Geometry
    Trigonometry
    Algebra
    Calculus

    Return only the 10 subtopic names.
    """

        response = cls.generate_text(
            prompt
        )

        subtopics = [
            subtopic.strip()
            for subtopic in response.split("\n")
            if subtopic.strip()
        ]

        return subtopics
    @classmethod
    def generate_learning_content(
        cls,
        subtopic_name,
    ):

        prompt = f"""
    Create beginner-friendly learning content for:

    {subtopic_name}

    Requirements:
    - Explain the concept clearly.
    - Include a short introduction.
    - Include key points.
    - Include a simple example if applicable.
    - Use plain text.
    - Keep the content between 300 and 500 words.
    - Do not use markdown.
    """

        return cls.generate_text(
            prompt
        )
    @classmethod
    def generate_quiz(
        cls,
        subtopic_name,
        content
    ):

        prompt = f"""
You are an expert educational assessment generator.

Your task is to create a quiz based ONLY on the learning content provided below.

SUBTOPIC:
{subtopic_name}

LEARNING CONTENT:
{content}

INSTRUCTIONS:

1. Generate exactly 5 multiple-choice questions.
2. Every question must be answerable using ONLY the provided learning content.
3. Do not use outside knowledge.
4. Questions should be beginner-friendly.
5. Each question must have exactly 4 options:

   * option_a
   * option_b
   * option_c
   * option_d
6. Only one option must be correct.
7. correct_answer must contain only:

   * "A"
   * "B"
   * "C"
   * "D"
8. All options must be different.
9. Do not repeat questions.
10. Do not repeat answer choices across the same question.

OUTPUT RULES:

* Return ONLY valid JSON.
* Do NOT use markdown.
* Do NOT use ```json.
* Do NOT include explanations.
* Do NOT include introductory text.
* Do NOT include closing text.
* Do NOT include comments.
* Do NOT include any text before or after the JSON.

REQUIRED JSON FORMAT:

[
{{
"question": "What is a variable?",
"option_a": "A loop",
"option_b": "A container for storing data",
"option_c": "A module",
"option_d": "A database",
"correct_answer": "B"
}}
]

Return exactly 5 objects in the JSON array.
"""


        response = cls.generate_text(
            prompt
        )

        response = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        import json

        return json.loads(
            response
        )