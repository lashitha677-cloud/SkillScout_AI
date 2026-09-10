from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone

from .models import (
    Profile,
    StudentSkill,
    StudentProject,
    StudentCertification,
    Opportunity,
    Notification,
)

from .forms import (
    StudentSkillForm,
    ProfileForm,
    StudentProjectForm,
    StudentCertificationForm,
    OpportunityForm,
    StudentRegistrationForm,
)

from .matching import check_student_eligibility

def landing(request):
    return render(request, "landing.html")

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            profile, created = Profile.objects.get_or_create(
    user=user,
    defaults={
        "role": "STUDENT"
    }
)

            if profile.role == "STUDENT":
                return redirect("student_dashboard")

            elif profile.role == "STAFF":
                return redirect("staff_dashboard")

            elif profile.role == "HOD":
                return redirect("hod_dashboard")

            return redirect("landing")

        else:

            return render(
                request,
                "auth/login.html",
                {
                    "error": "Invalid username or password."
                }
            )

    return render(request, "auth/login.html")

@login_required
def hod_dashboard(request):

    opportunities = Opportunity.objects.all().order_by("-event_date")

    total_opportunities = Opportunity.objects.count()

    total_students = Profile.objects.filter(
        role="STUDENT"
    ).count()

    active_opportunities = Opportunity.objects.filter(
        event_date__gte=timezone.now().date()
    ).count()

    return render(
        request,
        "hod/dashboard.html",
        {
            "opportunities": opportunities,
            "total_opportunities": total_opportunities,
            "total_students": total_students,
            "active_opportunities": active_opportunities,
        }
    )

def skill_passport(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            "role": "STUDENT"
        }
    )

    # ADD SKILL
    if request.method == "POST":

        form = StudentSkillForm(request.POST)

        if form.is_valid():

            skill = form.save(commit=False)

            skill.profile = profile

            skill.save()

            return redirect("skill_passport")

    else:

        form = StudentSkillForm()

    # GET STUDENT DATA
    skills = StudentSkill.objects.filter(
        profile=profile
    )

    projects = StudentProject.objects.filter(
        profile=profile
    )

    certifications = StudentCertification.objects.filter(
        profile=profile
    )

    return render(
        request,
        "student/skill_passport.html",
        {
            "profile": profile,
            "skills": skills,
            "projects": projects,
            "certifications": certifications,
            "form": form,
        }
    )

@login_required
def student_dashboard(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            "role": "STUDENT"
        }
    )

    skills_count = StudentSkill.objects.filter(
        profile=profile
    ).count()

    projects_count = StudentProject.objects.filter(
        profile=profile
    ).count()

    certifications_count = StudentCertification.objects.filter(
        profile=profile
    ).count()

    opportunities_count = Opportunity.objects.count()

    return render(
        request,
        "student/dashboard.html",
        {
            "profile": profile,
            "skills_count": skills_count,
            "projects_count": projects_count,
            "certifications_count": certifications_count,
            "opportunities_count": opportunities_count,
        }
    )

def edit_skill(request, skill_id):

    skill = StudentSkill.objects.get(
        id=skill_id,
        profile__user=request.user
    )

    if request.method == "POST":

        form = StudentSkillForm(
            request.POST,
            instance=skill
        )

        if form.is_valid():

            form.save()

            return redirect("skill_passport")

    else:

        form = StudentSkillForm(
            instance=skill
        )

    return render(
        request,
        "student/edit_skill.html",
        {
            "form": form,
            "skill": skill,
        }
    )


def delete_skill(request, skill_id):

    skill = StudentSkill.objects.get(
        id=skill_id,
        profile__user=request.user
    )

    if request.method == "POST":

        skill.delete()

        return redirect("skill_passport")

    return render(
        request,
        "student/delete_skill.html",
        {
            "skill": skill,
        }
    )

def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            "role": "STUDENT"
        }
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():
            form.save()

            return redirect("skill_passport")

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        "student/edit_profile.html",
        {
            "form": form,
            "profile": profile,
        }
    )

def student_projects(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            "role": "STUDENT"
        }
    )

    if request.method == "POST":

        form = StudentProjectForm(request.POST)

        if form.is_valid():

            project = form.save(commit=False)

            project.profile = profile

            project.save()

            return redirect("student_projects")

    else:

        form = StudentProjectForm()

    projects = StudentProject.objects.filter(
        profile=profile
    )

    return render(
        request,
        "student/projects.html",
        {
            "form": form,
            "projects": projects,
            "profile": profile,
        }
    )

def edit_project(request, project_id):

    project = StudentProject.objects.get(
        id=project_id,
        profile__user=request.user
    )

    if request.method == "POST":

        form = StudentProjectForm(
            request.POST,
            instance=project
        )

        if form.is_valid():

            form.save()

            return redirect("student_projects")

    else:

        form = StudentProjectForm(
            instance=project
        )

    return render(
        request,
        "student/edit_project.html",
        {
            "form": form,
            "project": project,
        }
    )


from django.shortcuts import get_object_or_404, redirect

def delete_project(request, project_id):
    profile = request.user.profile

    project = get_object_or_404(
        StudentProject,
        id=project_id,
        profile=profile
    )

    project.delete()

    return redirect("student_projects")

def student_certifications(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            "role": "STUDENT"
        }
    )

    if request.method == "POST":

        form = StudentCertificationForm(request.POST)

        if form.is_valid():

            certification = form.save(commit=False)

            certification.profile = profile

            certification.save()

            return redirect("student_certifications")

    else:

        form = StudentCertificationForm()

    certifications = StudentCertification.objects.filter(
        profile=profile
    )

    return render(
        request,
        "student/certifications.html",
        {
            "form": form,
            "certifications": certifications,
            "profile": profile,
        }
    )

def edit_certification(request, certification_id):

    certification = StudentCertification.objects.get(
        id=certification_id,
        profile__user=request.user
    )

    if request.method == "POST":

        form = StudentCertificationForm(
            request.POST,
            instance=certification
        )

        if form.is_valid():

            form.save()

            return redirect("student_certifications")

    else:

        form = StudentCertificationForm(
            instance=certification
        )

    return render(
        request,
        "student/edit_certification.html",
        {
            "form": form,
            "certification": certification,
        }
    )

def delete_certification(request, certification_id):

    certification = StudentCertification.objects.get(
        id=certification_id,
        profile__user=request.user
    )

    if request.method == "POST":

        certification.delete()

        return redirect("student_certifications")

    return render(
        request,
        "student/delete_certification.html",
        {
            "certification": certification,
        }
    )

def create_opportunity(request):

    if request.method == "POST":

        form = OpportunityForm(request.POST)

        if form.is_valid():

            opportunity = form.save()

            messages.success(
                request,
                f"'{opportunity.title}' was created successfully!"
            )

            return redirect("opportunity_list")

    else:

        form = OpportunityForm()

    opportunities = Opportunity.objects.all().order_by("-created_at")

    return render(
        request,
        "opportunities/opportunity_list.html",
        {
            "form": form,
            "opportunities": opportunities,
        }
    )

def opportunity_matches(request, opportunity_id):

    if not request.user.is_authenticated:
        return redirect("login")

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role not in ["STAFF", "HOD"]:
        return redirect("skill_passport")

    opportunity = Opportunity.objects.get(
        id=opportunity_id
    )

    profiles = Profile.objects.filter(
        role="STUDENT"
    ).select_related("user")

    results = []

    for student_profile in profiles:

        result = check_student_eligibility(
            student_profile,
            opportunity
        )

        if result["eligible"]:

            Notification.objects.get_or_create(
                profile=student_profile,
                title="New Opportunity Match",
                message=(
                    f"You are eligible for "
                    f"'{opportunity.title}' "
                    f"with a "
                    f"{result['match_percentage']}% match."
                )
            )

        results.append({
            "profile": student_profile,
            "result": result,
        })

    results.sort(
        key=lambda item: item["result"]["match_percentage"],
        reverse=True
    )

    eligible_count = sum(
        1
        for item in results
        if item["result"]["eligible"]
    )

    return render(
        request,
        "opportunities/matches.html",
        {
            "opportunity": opportunity,
            "results": results,
            "eligible_count": eligible_count,
            "user_role": profile.role,
        }
    )

@login_required
def staff_dashboard(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "STAFF":
        return redirect("student_dashboard")

    opportunities = Opportunity.objects.all().order_by("-created_at")

    return render(
        request,
        "staff/dashboard.html",
        {
            "opportunities": opportunities,
        }
    )

@login_required
def edit_opportunity(request, opportunity_id):

    opportunity = get_object_or_404(
        Opportunity,
        id=opportunity_id
    )

    if request.method == "POST":

        form = OpportunityForm(
            request.POST,
            instance=opportunity
        )

        if form.is_valid():
            form.save()
            return redirect("staff_dashboard")

    else:

        form = OpportunityForm(
            instance=opportunity
        )

    return render(
        request,
        "opportunities/edit_opportunity.html",
        {
            "form": form,
            "opportunity": opportunity,
        }
    )

@login_required
def delete_opportunity(request, opportunity_id):

    opportunity = get_object_or_404(
        Opportunity,
        id=opportunity_id
    )

    if request.method == "POST":
        opportunity.delete()
        messages.success(
            request,
            "Opportunity deleted successfully."
        )
        return redirect("staff_dashboard")

    return render(
        request,
        "opportunities/delete_opportunity.html",
        {
            "opportunity": opportunity,
        }
    )

def logout_view(request):
    logout(request)
    return redirect("login")

def hod_opportunities(request):
    opportunities = Opportunity.objects.all().order_by("-event_date")

    return render(
        request,
        "hod/opportunities.html",
        {
            "opportunities": opportunities,
        }
    )

@login_required
def student_notifications(request):

    profile = Profile.objects.get(
        user=request.user
    )

    notifications = Notification.objects.filter(
        profile=profile
    ).order_by("-created_at")

    return render(
        request,
        "student/notifications.html",
        {
            "notifications": notifications,
        }
    )


def student_register(request):
    if request.user.is_authenticated:
        return redirect("student_dashboard")

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            Profile.objects.create(
                user=user,
                role="STUDENT"
            )

            login(request, user)

            return redirect("student_dashboard")

    else:
        form = StudentRegistrationForm()

    return render(
        request,
        "auth/register.html",
        {"form": form}
    )