from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone

import json

from resumes.models import Resume

from .forms import InterviewForm

from django.db.models import Avg, Max

from .roles import INTERVIEW_ROLES


from .models import (
    InterviewSession,
    Conversation,
    InterviewReport,
    AnswerEvaluation
)

from .services.groq import (
    start_interview,
    continue_interview,
    generate_report,
    evaluate_answer,
    evaluate_code
)

# ==========================================
# ROLE SELECTION
# ==========================================

@login_required
def role_selection(request):

    if request.method == "POST":

        form = InterviewForm(request.POST)

        if form.is_valid():

            role = form.cleaned_data["role"]
            experience = form.cleaned_data["experience"]

            resume = Resume.objects.get(user=request.user)

            interview = InterviewSession.objects.create(
                user=request.user,
                role=role,
                experience=experience,
                question_count=0
            )

            first_question = start_interview(
                resume,
                role,
                experience
            )

            Conversation.objects.create(
                interview=interview,
                speaker="AI",
                message=first_question
            )

            return redirect(
                "voice_interview",
                interview.id
            )

    else:

        form = InterviewForm()

    return render(
        request,
        "interview/role_selection.html",
        {
            "form": form,
            "roles": INTERVIEW_ROLES,
        }
    )


# ==========================================
# VOICE INTERVIEW
# ==========================================

@login_required
def voice_interview(request, interview_id):

    interview = InterviewSession.objects.get(
        id=interview_id,
        user=request.user
    )

    first_question = interview.messages.first().message

    return render(
        request,
        "interview/voice_interview.html",
        {
            "interview": interview,
            "first_question": first_question
           
        }
    )


# ==========================================
# RECEIVE USER ANSWER
# ==========================================

@csrf_exempt
@require_POST
@login_required
def respond(request, interview_id):

    interview = InterviewSession.objects.get(
        id=interview_id,
        user=request.user
    )

    data = json.loads(request.body)

    answer = data.get("answer", "").strip()
    answer_type = data.get("type", "voice")

    last_ai_question = (
    interview.messages
    .filter(speaker="AI")
    .order_by("-created_at")
    .first()
    )

    
    if answer != "No response" and len(answer.split()) < 3:

        return JsonResponse({

            "finished": False,

            "question": last_ai_question.message,

            "question_number": interview.question_count

    })

    # Save user answer   

    user_message = Conversation.objects.create(
        interview=interview,
        speaker="USER",
        message=answer
)

    last_ai_question = (
         interview.messages
        .filter(speaker="AI")
        .order_by("-created_at")
        .first()
)

    if answer_type == "coding":
        evaluation = evaluate_code(
            last_ai_question.message,
            answer
    )
    else:
        evaluation = evaluate_answer(
            last_ai_question.message,
            answer
    )


    AnswerEvaluation.objects.create(
        conversation=user_message,
        technical_score=evaluation["technical_score"],
        communication_score=evaluation["communication_score"],
        confidence_score=evaluation["confidence_score"],
        feedback=evaluation["feedback"]
)
    
    # Increase question count

    interview.question_count += 1

    interview.save()
    
    print("QUESTION COUNT:", interview.question_count)

    resume = Resume.objects.get(
        user=request.user
    )

    # =====================================
    # END INTERVIEW AFTER 15 QUESTIONS
    # =====================================

    if interview.question_count >= 15:

        interview.status = "Completed"

        interview.ended_at = timezone.now()

        interview.save()

        report = generate_report(
            resume,
            interview
        )

        InterviewReport.objects.update_or_create(

            interview=interview,

            defaults={

                "overall_score":
                    report.get("overall_score", 0),

                "technical_score":
                    report.get("technical_score", 0),

                "communication_score":
                    report.get("communication_score", 0),

                "confidence_score":
                    report.get("confidence_score", 0),

                "strengths":
                    "\n".join(
                        report.get("strengths", [])
                    ),

                "weaknesses":
                    "\n".join(
                        report.get("weaknesses", [])
                    ),

                "suggestions":
                    "\n".join(
                        report.get("suggestions", [])
                    )

            }

        )

        return JsonResponse({

            "finished": True,

            "redirect_url":
                f"/interview/report/{interview.id}/"

        })

    # =====================================
    # CONTINUE INTERVIEW
    # =====================================

    result = continue_interview(
    interview,
    answer
)

    Conversation.objects.create(

    interview=interview,

    speaker="AI",

    message=result["question"]

)

    return JsonResponse({

    "finished": False,

    "type": result["type"],

    "question": result["question"],

    "question_number": interview.question_count

})


# ==========================================
# REPORT PAGE
# ==========================================

@login_required
def interview_report(request, interview_id):

    interview = InterviewSession.objects.get(

        id=interview_id,

        user=request.user

    )

    report = InterviewReport.objects.get(

        interview=interview

    )

    return render(

        request,

        "interview/report.html",

        {

            "interview": interview,

            "report": report

        }

    )


# ==========================================
# PREVIOUS REPORTS
# ==========================================

@login_required
def previous_reports(request):

    reports = InterviewReport.objects.filter(

        interview__user=request.user

    ).order_by(

        "-generated_at"

    )

    return render(

        request,

        "interview/previous_reports.html",

        {

            "reports": reports

        }

    )
    
@login_required
def profile(request):

    resume = Resume.objects.filter(user=request.user).first()

    reports = InterviewReport.objects.filter(
        interview__user=request.user
    )

    total_interviews = reports.count()

    average_score = reports.aggregate(
        Avg("overall_score")
    )["overall_score__avg"] or 0

    highest_score = reports.aggregate(
        Max("overall_score")
    )["overall_score__max"] or 0

    context = {
        "resume": resume,
        "total_interviews": total_interviews,
        "average_score": round(average_score, 1),
        "highest_score": highest_score,
    }

    return render(
        request,
        "interview/profile.html",
        context
    )