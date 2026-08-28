import json

from interview.models import AnswerEvaluation
from django.conf import settings
from groq import Groq

client = Groq(
    api_key=settings.GROQ_API_KEY
)


# ==========================================
# START INTERVIEW
# ==========================================

def start_interview(resume, role, experience):

    return (
        "Good morning! Welcome to your AI mock interview. "
        "Thank you for joining us today. "
        "This interview will consist of 15 questions. "
        "To begin, could you please introduce yourself and walk me through your background?"
    )




# ==========================================
# CONTINUE INTERVIEW
# ==========================================

def continue_interview(interview, candidate_answer):
    
    resume = interview.user.resume

    messages = [
        {
            "role": "system",
            "content": f"""
            

You are a Senior Technical Interviewer with over 15 years of experience interviewing candidates at top multinational companies such as Microsoft, Google, Amazon, Deloitte, Accenture, IBM, TCS, Infosys, Cognizant, Capgemini, Oracle, and Adobe.

Your responsibility is to conduct a highly realistic technical interview exactly like a human interviewer.

The interview must feel natural, conversational, and professional.

Candidate Information

Role:
{interview.role}

Experience:
{interview.experience}

Resume Details:
{resume.extracted_text}

Skills:
{resume.skills}

Projects:
{resume.projects}

Education:
{resume.education}

Certifications:
{resume.certifications}

Latest Candidate Answer:
{candidate_answer}

Current Interview Progress

Current Question Number:
{interview.question_count}

Interview Flow Rules

Question 1:
The candidate has already introduced themselves.

Question 2:
Ask one follow-up question about their introduction.
Examples:
- What motivated you to choose this career?
- Could you tell me more about your academic journey?
- What interested you in applying for this role?

Question 3:
Discuss the candidate's projects or internship experience.

Questions 4–8:
Ask technical questions based on the candidate's resume, skills, and previous answers.

Questions 9–11:
Ask practical scenario-based or debugging questions.

Questions 12–13:
Ask one or two coding questions if appropriate for the role.

Questions 14–15:
Ask HR or behavioral questions such as teamwork, strengths, weaknesses, conflict resolution, or future goals.

Do not mention question numbers to the candidate.
Transition naturally between topics.

Total Questions:
15

Instructions

• The current interviewer question number is {interview.question_count}.

• Continue asking questions until the interviewer has asked exactly 15 questions.

• If the current question number is 14, ask the final interview question.

• Never end the interview before the fifteenth question.

• Never tell the candidate the current question number.

• Ask ONLY ONE question.

• Never ask multiple questions together.

• Never number the questions.

• Never say:
  "Technical Question"
  "Behavioral Question"
  "Next Question"
  "Let's move on"
  "Now let's discuss..."
  "Question 5"

• Continue the conversation naturally.

• Remember everything discussed previously.

• If the candidate gives a weak answer, ask a deeper follow-up.

• If the candidate gives a strong answer, move naturally into another relevant topic.

• Frequently ask:
    Why?
    How?
    What if?
    Can you explain further?

• Ask follow-up questions whenever appropriate.

• Base questions primarily on the candidate's resume and previous answers.

• If the resume contains projects, explore architecture, implementation, challenges, debugging, optimization, scalability, deployment, security, APIs, databases, testing, and design decisions.

• Ask practical questions instead of textbook definitions.

Examples:

Instead of:
"What is Python?"

Ask:
"When would you prefer a generator over returning a list?"

Instead of:
"What is SQL?"

Ask:
"You mentioned using MySQL in your project. Which query was the most difficult to write and why?"

Instead of:
"What is OOP?"

Ask:
"Where exactly did you apply inheritance or polymorphism in your project?"

Interview Style

Conduct the interview exactly like a real interviewer.

The conversation should naturally move between:

• Resume
• Projects
• Python
• Django/Flask/FastAPI (depending on resume)
• SQL
• OOP
• APIs
• Git
• Debugging
• Optimization
• Data Structures
• Problem Solving
• Software Engineering
• Behavioral Questions
• Situational Questions

Do NOT force this order.

Choose the next question based on the conversation.

Challenge the candidate when appropriate.

Sometimes ask scenario-based questions.

Sometimes ask debugging questions.

Sometimes ask project deep dives.

Sometimes ask why a particular design choice was made.

Do not repeat previous questions.

Do not ask unrelated questions.

The interview should feel like a live technical interview.

The interview must continue until exactly FIFTEEN interviewer questions have been asked.

Never end the interview before the fifteenth question.

Return ONLY valid JSON.

For normal interview questions return:

{{
    "type": "voice",
    "question": "Your interview question"
}}

For coding questions return:

{{
    "type": "coding",
    "question": "Write a Python program..."
}}

Rules:

• Ask approximately 2 or 3 coding questions during the 15-question interview.
• Coding questions must be based on the candidate's skills and projects.
• Never mix coding and voice in one question.
• Return ONLY JSON.

"""
        }
    ]


    response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=messages,
    temperature=0.2
)

    result = response.choices[0].message.content.strip()

    print("AI RAW RESPONSE:")
    print(result)

    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    return json.loads(result)
# ==========================================
# FINAL REPORT
# ==========================================

def evaluate_answer(question, answer):

    prompt = f"""
You are a Senior Technical Interview Evaluator.

Evaluate ONLY this single interview answer.

Interview Question:
{question}

Candidate Answer:
{answer}

Rules:

1. Give scores between 0 and 10.

2. If the answer is irrelevant, empty, "I don't know",
one word, or silence,
give very low scores.

3. Be strict.

Return ONLY valid JSON.

Format:

{{
    "technical_score": 0,
    "communication_score": 0,
    "confidence_score": 0,
    "feedback": "Short constructive feedback"
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are an expert interview evaluator."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip()

    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    return json.loads(result)


def evaluate_code(question, code):

    prompt = f"""
You are a Senior Software Engineer conducting a coding interview.

Evaluate ONLY this coding answer.

Coding Question:
{question}

Candidate Code:
{code}

Rules:

1. Give scores between 0 and 10.

2. Evaluate:
- Correctness
- Code quality
- Communication (comments, readability, naming)
- Confidence (overall quality)

3. Mention time complexity and space complexity inside the feedback.

Return ONLY valid JSON.

{{
    "technical_score": 0,
    "communication_score": 0,
    "confidence_score": 0,
    "feedback": "Mention correctness, time complexity, space complexity and suggestions."
}}
"""

    response = client.chat.completions.create(

        
        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": "You are an expert coding interviewer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0

    )

    result = response.choices[0].message.content.strip()

    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    return json.loads(result)


def generate_report(resume, interview):

    evaluations = AnswerEvaluation.objects.filter(
        conversation__interview=interview
    )

    if not evaluations.exists():

        return {

            "overall_score": 0,

            "technical_score": 0,

            "communication_score": 0,

            "confidence_score": 0,

            "strengths": [],

            "weaknesses": [],

            "suggestions": []

        }

    # -----------------------------
    # Calculate Scores
    # -----------------------------

    total_technical = sum(
        e.technical_score for e in evaluations
    )

    total_communication = sum(
        e.communication_score for e in evaluations
    )

    total_confidence = sum(
        e.confidence_score for e in evaluations
    )

    count = evaluations.count()

    # Average score out of 10
    technical = total_technical / count
    communication = total_communication / count
    confidence = total_confidence / count

    # Convert to percentage
    technical_percent = round(technical * 10)
    communication_percent = round(communication * 10)
    confidence_percent = round(confidence * 10)

    overall = round(
        (
            technical_percent +
            communication_percent +
            confidence_percent
        ) / 3
    )

    # -----------------------------
    # Build Interview Transcript
    # -----------------------------

    transcript = ""

    conversations = interview.messages.all().order_by("created_at")

    for chat in conversations:

        transcript += f"{chat.speaker}: {chat.message}\n"

    # -----------------------------
    # Ask AI ONLY for qualitative analysis
    # -----------------------------

    prompt = f"""
The interview has finished.

Below is the interview transcript.

{transcript}

The calculated scores are:

Overall Score : {overall}

Technical Score : {technical_percent}

Communication Score : {communication_percent}

Confidence Score : {confidence_percent}

Your task is ONLY to generate:

1. Strengths
2. Weaknesses
3. Suggestions

DO NOT change the scores.

Return ONLY valid JSON.

{{
    "strengths":[
        "...",
        "...",
        "..."
    ],

    "weaknesses":[
        "...",
        "..."
    ],

    "suggestions":[
        "...",
        "..."
    ]
}}
"""

    response = client.chat.completions.create(

        
        model="openai/gpt-oss-120b",

        messages=[

            {

                "role": "system",

                "content":
                "You are an expert interview evaluator."

            },

            {

                "role": "user",

                "content": prompt

            }

        ],

        temperature=0.2

    )

    result = response.choices[0].message.content.strip()

    if result.startswith("```"):

        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    analysis = json.loads(result)

    return {

        "overall_score": overall,

        "technical_score": technical_percent,

        "communication_score": communication_percent,

        "confidence_score": confidence_percent,

        "strengths": analysis["strengths"],

        "weaknesses": analysis["weaknesses"],

        "suggestions": analysis["suggestions"]

    }