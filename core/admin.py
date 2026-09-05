from django.contrib import admin
from .models import ( Profile, StudentSkill, StudentProject, StudentCertification,
                     Opportunity, )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "department",
        "year",
    )

    list_filter = (
        "role",
        "department",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
    )

@admin.register(StudentSkill)
class StudentSkillAdmin(admin.ModelAdmin):

    list_display = (
        "profile",
        "skill_name",
        "skill_level",
        "years_experience",
    )

    list_filter = (
        "skill_level",
    )

    search_fields = (
        "skill_name",
        "profile__user__username",
    )

@admin.register(StudentProject)
class StudentProjectAdmin(admin.ModelAdmin):

    list_display = (
        "profile",
        "project_title",
        "technologies",
        "project_type",
    )

    search_fields = (
        "project_title",
        "technologies",
        "profile__user__username",
    )

    list_filter = (
        "project_type",
    )

@admin.register(StudentCertification)
class StudentCertificationAdmin(admin.ModelAdmin):

    list_display = (
        "profile",
        "certificate_name",
        "issuing_organization",
        "issue_year",
    )

    search_fields = (
        "certificate_name",
        "issuing_organization",
        "profile__user__username",
    )

    list_filter = (
        "issue_year",
        "issuing_organization",
    )

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "opportunity_type",
        "minimum_skill_level",
        "event_date",
        "created_at",
    )

    search_fields = (
        "title",
        "required_skills",
    )

    list_filter = (
        "opportunity_type",
        "minimum_skill_level",
    )