from django.urls import path
from django.contrib.auth import views as auth_views
from .views import landing, login_view, skill_passport, edit_profile, student_register
from .ai_views import ai_assistant
from . import views


urlpatterns = [
    path("", landing, name="landing"),
    path("login/", login_view, name="login"),
    path("register/", student_register, name="student_register"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("student/skills/", skill_passport, name="skill_passport"),
    path("student/profile/edit/", edit_profile, name="edit_profile"),
    path("student/skills/<int:skill_id>/edit/", views.edit_skill, name="edit_skill"),
    path("student/skills/<int:skill_id>/delete/", views.delete_skill, name="delete_skill"),
    path("student/projects/", views.student_projects, name="student_projects"),
    path("student/projects/<int:project_id>/edit/", views.edit_project, name="edit_project"),
    path("student/projects/<int:project_id>/delete/", views.delete_project, name="delete_project"),
    path("student/certifications/", views.student_certifications, name="student_certifications"),
    path("student/certifications/<int:certification_id>/edit/", views.edit_certification, name="edit_certification"),
    path("student/certifications/<int:certification_id>/delete/", views.delete_certification, name="delete_certification"),
    path("opportunities/", views.create_opportunity, name="opportunity_list"),
    path("opportunities/<int:opportunity_id>/matches/", views.opportunity_matches, name="opportunity_matches"),
    path("staff/dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("opportunities/<int:opportunity_id>/edit/", views.edit_opportunity, name="edit_opportunity"),
    path("opportunities/<int:opportunity_id>/delete/", views.delete_opportunity, name="delete_opportunity"),
    path("hod/dashboard/", views.hod_dashboard, name="hod_dashboard"),
    path("hod/opportunities/", views.hod_opportunities, name="hod_opportunities"),
    path("ai-assistant/", ai_assistant, name="ai_assistant"),
    path("student/notifications/", views.student_notifications, name="student_notifications"),
]