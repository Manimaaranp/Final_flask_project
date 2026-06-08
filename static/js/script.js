// ======================
// API HELPER
// ======================

const API = {
    get: async (url) => {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error("Request failed");
        }

        return await response.json();
    },

    post: async (url, data) => {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || "Request failed");
        }

        return await response.json();
    }
};

// ======================
// INDEX PAGE
// ======================

async function generateRoadmap() {

    const careerInput =
        document.getElementById("careerInput");

    if (!careerInput) return;

    const careerName =
        careerInput.value.trim();

    if (!careerName) {
        alert("Please enter a career name");
        return;
    }

    sessionStorage.setItem(
        "career_name",
        careerName
    );

    try {

        await API.post(
            "/api/generate-roadmap",
            {
                career_name: careerName
            }
        );

        window.location.href =
            "/roadmap";

    } catch (error) {

        alert(error.message);

    }
}

// ======================
// ROADMAP PAGE
// ======================

async function loadRoadmap() {

    const container =
        document.getElementById(
            "roadmapContainer"
        );

    if (!container) return;

    const careerName =
        sessionStorage.getItem(
            "career_name"
        );

    if (!careerName) {

        container.innerHTML =
            "<p>No career selected.</p>";

        return;
    }

    try {

        const data =
            await API.post(
                "/api/generate-roadmap",
                {
                    career_name: careerName
                }
            );

        container.innerHTML =
            data.topics
                .map(topic => `
                    <div
                        class="card-box"
                        onclick="selectTopic('${topic}')"
                    >
                        ${topic}
                    </div>
                `)
                .join("");

    } catch (error) {

        container.innerHTML =
            `<p>${error.message}</p>`;

    }
}

function selectTopic(topicName) {

    sessionStorage.setItem(
        "topic_name",
        topicName
    );

    window.location.href =
        "/subtopic";
}

// ======================
// SUBTOPIC PAGE
// ======================

async function loadSubtopics() {

    const container =
        document.getElementById(
            "subtopicContainer"
        );

    if (!container) return;

    const topicName =
        sessionStorage.getItem(
            "topic_name"
        );

    if (!topicName) {

        container.innerHTML =
            "<p>No topic selected.</p>";

        return;
    }

    try {

        const data =
            await API.post(
                "/api/generate-subtopics",
                {
                    topic_name: topicName
                }
            );

        const progress =
            await API.get(
                "/api/progress"
            );

        const completedSubtopics =
            progress.completed_subtopic_names || [];

        container.innerHTML =
            data.subtopics
                .map(subtopic => {

                    const completed =
                        completedSubtopics.includes(
                            subtopic
                        );

                    return `
                        <div
                            class="
                                card-box
                                ${completed
                                    ? "completed-subtopic"
                                    : ""}
                            "
                            onclick="
                                selectSubtopic(
                                    '${subtopic}'
                                )
                            "
                        >
                            ${completed ? "✅ " : ""}
                            ${subtopic}
                        </div>
                    `;
                })
                .join("");

    } catch (error) {

        container.innerHTML =
            `<p>${error.message}</p>`;

    }
}

function selectSubtopic(subtopicName) {

    sessionStorage.setItem(
        "subtopic_name",
        subtopicName
    );

    window.location.href =
        "/content";
}

// ======================
// CONTENT PAGE
// ======================

async function loadContent() {

    const container =
        document.getElementById(
            "contentContainer"
        );

    if (!container) return;

    const subtopicName =
        sessionStorage.getItem(
            "subtopic_name"
        );

    if (!subtopicName) {

        container.innerHTML =
            "<p>No subtopic selected.</p>";

        return;
    }

    try {

        const data =
            await API.post(
                "/api/generate-content",
                {
                    subtopic_name:
                        subtopicName
                }
            );

        container.innerHTML = `
            <div class="card-box">
                <h4>${data.subtopic}</h4>
                <p>${data.content}</p>

                <button
                    class="btn btn-primary mt-3"
                    onclick="goToQuiz()"
                >
                    Take Quiz
                </button>
            </div>
        `;

    } catch (error) {

        container.innerHTML =
            `<p>${error.message}</p>`;

    }
}

function goToQuiz() {

    window.location.href =
        "/quiz";
}

// ======================
// QUIZ PAGE
// ======================

async function loadQuiz() {

    const container =
        document.getElementById(
            "quizContainer"
        );

    if (!container) return;

    const subtopicName =
        sessionStorage.getItem(
            "subtopic_name"
        );

    if (!subtopicName) {

        container.innerHTML =
            "<p>No subtopic selected.</p>";

        return;
    }

    try {

        const data =
            await API.post(
                "/api/generate-quiz",
                {
                    subtopic_name:
                        subtopicName
                }
            );

        container.innerHTML =
            data.quiz
                .map((quiz, index) => `
                    <div
                        class="card-box mb-4"
                        id="quiz-card-${quiz.id}"
                    >
                        <h5>
                            Q${index + 1}.
                            ${quiz.question}
                        </h5>

                        <label>
                            <input
                                type="radio"
                                name="quiz_${quiz.id}"
                                value="A"
                            >
                            ${quiz.option_a}
                        </label>
                        <br>

                        <label>
                            <input
                                type="radio"
                                name="quiz_${quiz.id}"
                                value="B"
                            >
                            ${quiz.option_b}
                        </label>
                        <br>

                        <label>
                            <input
                                type="radio"
                                name="quiz_${quiz.id}"
                                value="C"
                            >
                            ${quiz.option_c}
                        </label>
                        <br>

                        <label>
                            <input
                                type="radio"
                                name="quiz_${quiz.id}"
                                value="D"
                            >
                            ${quiz.option_d}
                        </label>
                        <br>

                        <button
                            id="submit-btn-${quiz.id}"
                            class="btn btn-success mt-2"
                            onclick="submitQuiz(${quiz.id})"
                        >
                            Submit Answer
                        </button>
                    </div>
                `)
                .join("");

    } catch (error) {

        container.innerHTML =
            `<p>${error.message}</p>`;

    }
}
const completedQuestions =
    new Set();
async function submitQuiz(
    quizId
) {

    const selectedOption =
        document.querySelector(
            `input[name="quiz_${quizId}"]:checked`
        );

    if (!selectedOption) {

        alert(
            "Please select an answer."
        );

        return;
    }

    try {

        const result =
            await API.post(
                "/api/submit-quiz",
                {
                    quiz_id: quizId,
                    selected_answer:
                        selectedOption.value
                }
            );

        if (result.correct) {

            const card =
                document.getElementById(
                    `quiz-card-${quizId}`
                );

            if (card) {

                card.style.backgroundColor =
                    "#d4edda";

                card.style.border =
                    "2px solid #28a745";

            }

            const radios =
                document.querySelectorAll(
                    `input[name="quiz_${quizId}"]`
                );

            radios.forEach(
                radio => radio.disabled = true
            );

            const submitBtn =
                document.getElementById(
                    `submit-btn-${quizId}`
                );

            if (submitBtn) {

                submitBtn.disabled = true;

                submitBtn.innerText =
                    "Completed";

            }

            if (
                !completedQuestions.has(
                    quizId
                )
            ) {

                completedQuestions.add(
                    quizId
                );

            }

            if (
                completedQuestions.size === 5
            ) {

                alert(
                    "Quiz completed successfully!"
                );

                window.location.href =
                    "/subtopic";

            }

        }
         else {

            alert(
                `${result.message}
Correct Answer: ${result.correct_answer}`
            );

        }

    } catch (error) {

        alert(error.message);

    }
}

// ======================
// PROGRESS PAGE
// ======================

    async function loadProgress() {

        const progressBar =
            document.getElementById(
                "progressBar"
            );

        const progressText =
            document.getElementById(
                "progressText"
            );

        if (
            !progressBar ||
            !progressText
        ) {
            return;
        }

        try {

            const data =
                await API.get(
                    "/api/progress"
                );

            progressBar.style.width =
                `${data.progress_percentage}%`;

            progressBar.innerText =
                `${data.progress_percentage}%`;

            progressText.innerText =
                `${data.completed_subtopics} / ${data.total_subtopics} completed`;

        } catch (error) {

            console.error(error);

        }
    }
    if (
        window.location.pathname ===
        "/subtopic"
    ) {

        loadProgress();

    }





// ======================
// AUTO LOAD
// ======================

window.onload = function () {

    if (
        document.getElementById(
            "roadmapContainer"
        )
    ) {
        loadRoadmap();
    }

    if (
        document.getElementById(
            "subtopicContainer"
        )
    ) {
        loadSubtopics();
    }

    if (
        document.getElementById(
            "contentContainer"
        )
    ) {
        loadContent();
    }

    if (
        document.getElementById(
            "quizContainer"
        )
    ) {
        loadQuiz();
    }

    if (
        document.getElementById(
            "progressBar"
        )
    ) {
        loadProgress();
    }
};