from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ResumeForm
from .models import Resume

from .services.parser import extract_text_from_pdf
from .services.gemini import analyze_resume


@login_required
def upload_resume(request):

    resume = Resume.objects.filter(user=request.user).first()

    if request.method == "POST":

        form = ResumeForm(
            request.POST,
            request.FILES,
            instance=resume
        )

        if form.is_valid():

            try:
                uploaded_resume = form.save(commit=False)
                uploaded_resume.user = request.user
                uploaded_resume.save()

                print("✅ Resume uploaded")

                # Extract text
                text = extract_text_from_pdf(uploaded_resume.resume.path)
                uploaded_resume.extracted_text = text

                print("✅ PDF extracted")
                print("Characters:", len(text))

                # AI Analysis
                data = analyze_resume(text)

                print("✅ Gemini Response")
                print(data)

                uploaded_resume.skills = "\n".join(data.get("skills", []))

                uploaded_resume.projects = "\n".join(data.get("projects", []))

                uploaded_resume.education = "\n".join(data.get("education", []))

                uploaded_resume.certifications = "\n".join(data.get("certifications", []))

                uploaded_resume.save()

                messages.success(request, "Resume uploaded and analyzed successfully!")

                return redirect("dashboard")

            except Exception as e:
                print("❌ ERROR:", e)
                messages.error(request, f"Error: {e}")

        else:
            print(form.errors)

    else:
        form = ResumeForm(instance=resume)

    return render(
        request,
        "resumes/upload.html",
        {
            "form": form,
            "resume": resume,
        },
    )