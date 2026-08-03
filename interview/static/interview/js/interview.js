const button = document.getElementById("startButton");
const skipButton = document.getElementById("skipButton");
console.log(skipButton);
const aiQuestion = document.getElementById("aiQuestion");
const userSpeech = document.getElementById("userSpeech");

const status = document.getElementById("status");
const counter = document.getElementById("questionCounter");

const SILENCE_TIMEOUT = 60000; // 1 minute

const codingSection =
    document.getElementById("codingSection");

const codeEditor =
    document.getElementById("codeEditor");

const submitCodeButton =
    document.getElementById("submitCodeButton");

    
const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();

recognition.lang = "en-US";
recognition.interimResults = true;
recognition.continuous = false;

let interviewFinished = false;
let silenceTimer = null;
let autoSkipping = false;
// =========================
// INITIAL UI
// =========================

aiQuestion.innerHTML = "";
userSpeech.innerHTML = "Click Start Interview";

status.innerHTML = "🟢 Ready";

counter.innerHTML = "Question 1 / 15";


// =========================
// START INTERVIEW
// =========================

button.onclick = function () {

    button.disabled = true;

    const firstQuestion =
        document.getElementById("firstQuestion").value;

    speak("Your interview will start now.", function () {

        typeAndSpeak(firstQuestion, function () {

            recognition.start();

        });

    });

};


// =========================
// SPEAK
// =========================

function speak(text, callback) {

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";
    speech.rate = 1;
    speech.pitch = 1;

    speech.onend = function () {

        if (callback) {

            callback();

        }

    };

    window.speechSynthesis.speak(speech);

}


// =========================
// TYPE + SPEAK
// =========================

function typeAndSpeak(text, callback) {

    status.innerHTML = "🟢 AI Speaking...";

    aiQuestion.innerHTML = "";

    const words = text.split(" ");

    let index = 0;

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";
    speech.rate = 1;
    speech.pitch = 1;

    const typing = setInterval(() => {

        if (index < words.length) {

            aiQuestion.innerHTML += words[index] + " ";

            index++;

        }

    }, 150);

    speech.onend = function () {

        clearInterval(typing);

        aiQuestion.innerHTML = text;

        if (callback) {

            callback();

        }

    };

    window.speechSynthesis.speak(speech);

}

// =========================
// SILENCE TIMER
// =========================

function startSilenceTimer() {
    
    console.log("Timer started");

    clearTimeout(silenceTimer); 

    silenceTimer = setTimeout(function () {

        console.log("TIMEOUT REACHED");

        // Don't skip coding questions
        if (codingSection.style.display === "block") {
            return;
        }

        autoSkipping = true;
        recognition.stop();

        status.innerHTML = "⏰ Time's Up";

        userSpeech.innerHTML =
            "No response received.";

        speak(
            "I didn't receive your response within one minute. Let's move on to the next question.",
            function () {

                submitAnswer("No response", "voice");

            }
        );

    }, SILENCE_TIMEOUT);

}


function stopSilenceTimer() {

    clearTimeout(silenceTimer);

}


// =========================
// LISTENING
// =========================

recognition.onstart = function () {

    status.innerHTML = "🎤 Listening...";

    userSpeech.innerHTML = "Listening...";




};


// =========================
// SPEECH RESULT
// =========================

recognition.onresult = function (event) {

    // User started speaking, stop the timer
    stopSilenceTimer();

    status.innerHTML = "📝 Recording your answer...";

    let transcript = "";

    for (let i = event.resultIndex; i < event.results.length; i++) {

        transcript += event.results[i][0].transcript;

    }

    userSpeech.innerHTML = transcript;

};


function submitAnswer(answer, type = "voice") {

    // Stop the silence timer
    stopSilenceTimer();

    status.innerHTML = "🧠 Thinking...";

    const interviewId =
        document.getElementById("interviewId").value;

    fetch(`/interview/${interviewId}/respond/`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            answer: answer,
            type: type
        })

    })

    .then(response => response.json())

    .then(data => {

        // =========================
        // INTERVIEW COMPLETED
        // =========================

        if (data.finished) {

            interviewFinished = true;

            button.disabled = true;

            status.innerHTML = "✅ Interview Completed";

            counter.innerHTML = "Interview Finished";

            typeAndSpeak(
                "Thank you for your time. This concludes the interview.",
                function () {
                    window.location.href = data.redirect_url;
                }
            );

            return;
        }

        counter.innerHTML =
            `Question ${data.question_number + 1} / 15`;

        userSpeech.innerHTML = "";

        // =====================
        // VOICE QUESTION
        // =====================

        if (data.type === "voice") {

            codingSection.style.display = "none";

            typeAndSpeak(
                data.question,
                function () {

                    userSpeech.innerHTML = "🎤 Listening...";

        // Start the one-minute countdown here
                    startSilenceTimer();

                    setTimeout(function () {

                        recognition.start();

        }, 800);

    }
);

        }

        // =====================
        // CODING QUESTION
        // =====================

        else if (data.type === "coding") {

    // Stop any running silence timer
            stopSilenceTimer();

            recognition.stop();

            codingSection.style.display = "block";

            aiQuestion.innerHTML = data.question;

            codeEditor.value = "";

            status.innerHTML = "⌨️ Write your code";

    }

    })

    .catch(error => {

        console.error(error);

        status.innerHTML = "❌ Error";

        userSpeech.innerHTML = "Something went wrong.";

    });

}


// =========================
// USER FINISHED
// =========================

recognition.onend = function () {

    console.log("Recognition ended");

    if (interviewFinished) {
        return;
    }

    // If timeout triggered this stop,
    // don't restart recognition.
    if (autoSkipping) {

        autoSkipping = false;

        return;
    }

    const answer = userSpeech.innerText.trim();

    if (
        answer === "" ||
        answer === "Listening..."
    ) {


        if (!autoSkipping) {

            recognition.start();
        }

        return;

    }

    submitAnswer(answer, "voice");

};

// =========================
// SKIP QUESTION
// =========================

skipButton.onclick = function () {

    console.log("Skip button clicked!");

    autoSkipping = true;

    recognition.stop();

    userSpeech.innerHTML = "Question skipped.";

    submitAnswer("No response", "voice");
};

// =========================
// SUBMIT CODE
// =========================

submitCodeButton.onclick = function () {

    const code = codeEditor.value.trim();

    if (code === "") {

        alert("Please write your code.");

        return;

    }

    codingSection.style.display = "none";

    userSpeech.innerHTML = "Code Submitted";

    submitAnswer(code, "coding");

};

// =========================
// ERROR
// =========================

recognition.onerror = function (event) {

    console.log(event);

    // Ignore normal aborts
    if (event.error === "aborted") {
        return;
    }

    status.innerHTML = "❌ Microphone Error";

    userSpeech.innerHTML = event.error;

};