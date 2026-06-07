// ======================
// API HELPER (DRY CORE)
// ======================
const API = {
    get: (url) => fetch(url).then(res => res.json()),

    post: (url, data) =>
        fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        }).then(res => res.json())
};

// ======================
// INDEX → GENERATE ROADMAP
// ======================
function generateRoadmap() {
    const career = document.getElementById("careerInput").value;

    API.post("/generate-roadmap", { career })
        .then(() => {
            window.location.href = "/roadmap";
        });
}

// ======================
// LOGIN
// ======================
function login() {
    API.post("/login", {
        email: document.getElementById("loginEmail").value,
        password: document.getElementById("loginPassword").value
    });
}

// ======================
// SIGNUP
// ======================
function signup() {
    API.post("/signup", {
        email: document.getElementById("signupEmail").value,
        password: document.getElementById("signupPassword").value
    });
}

// ======================
// ROADMAP
// ======================
async function loadRoadmap() {
    const data = await API.get("/api/roadmap");

    document.getElementById("roadmapContainer").innerHTML =
        data.map(item =>
            `<div class="card-box" onclick="loadTopics(${item.id})">
                ${item.name}
            </div>`
        ).join("");
}

// ======================
// TOPICS
// ======================
async function loadTopics(careerId) {
    const data = await API.get(`/api/topic/${careerId}`);

    document.getElementById("topicContainer").innerHTML =
        data.map(item =>
            `<div class="card-box" onclick="loadContent(${item.id})">
                ${item.name}
            </div>`
        ).join("");
}

// ======================
// CONTENT
// ======================
async function loadContent(topicId) {
    const data = await API.get(`/api/content/${topicId}`);

    document.getElementById("contentContainer").innerHTML =
        `<div class="card-box">${data.content}</div>`;
}

// ======================
// QUIZ
// ======================
function submitQuiz() {
    API.post("/submit-quiz", {
        answers: getAnswers()
    });
}

function getAnswers() {
    return [...document.querySelectorAll("input[type=radio]:checked")]
        .map(el => el.value);
}

// ======================
// PROGRESS
// ======================
async function loadProgress() {
    const data = await API.get("/api/progress");

    document.getElementById("progressBar").style.width =
        data.progress + "%";

    document.getElementById("progressText").innerText =
        data.progress + "% completed";
}

// ======================
// AUTO LOAD
// ======================
window.onload = function () {
    if (document.getElementById("roadmapContainer")) loadRoadmap();
    if (document.getElementById("progressBar")) loadProgress();
};