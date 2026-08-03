from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from resumes.models import Resume


@login_required
def dashboard(request):

    resume = Resume.objects.filter(
        user=request.user
    ).first()

    context = {

        "resume": resume,

    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )