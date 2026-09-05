from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    ROLE_CHOICES = [
        ("STUDENT", "Student"),
        ("STAFF", "Staff"),
        ("HOD", "HOD"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="STUDENT"
    )

    department = models.CharField(
        max_length=100,
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class StudentSkill(models.Model):

    SKILL_LEVELS = [
        ("BEGINNER", "Beginner"),
        ("INTERMEDIATE", "Intermediate"),
        ("ADVANCED", "Advanced"),
        ("EXPERT", "Expert"),
    ]

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    skill_name = models.CharField(
        max_length=100
    )

    skill_level = models.CharField(
        max_length=20,
        choices=SKILL_LEVELS,
        default="BEGINNER"
    )

    years_experience = models.FloatField(
        default=0
    )

    def __str__(self):
        return f"{self.profile.user.username} - {self.skill_name}"

class StudentProject(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    project_title = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    technologies = models.CharField(
        max_length=300,
        blank=True
    )

    project_type = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return f"{self.profile.user.username} - {self.project_title}"

class StudentCertification(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="certifications"
    )

    certificate_name = models.CharField(
        max_length=150
    )

    issuing_organization = models.CharField(
        max_length=150
    )

    issue_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.profile.user.username} - {self.certificate_name}"

class Opportunity(models.Model):

    OPPORTUNITY_TYPES = [
        ("HACKATHON", "Hackathon"),
        ("INTERVIEW", "Interview"),
        ("PRESENTATION", "Presentation"),
        ("COMPETITION", "Competition"),
        ("OTHER", "Other"),
    ]

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    opportunity_type = models.CharField(
        max_length=30,
        choices=OPPORTUNITY_TYPES,
        default="OTHER"
    )

    required_skills = models.CharField(
        max_length=500,
        help_text="Enter skills separated by commas"
    )

    minimum_skill_level = models.CharField(
        max_length=20,
        choices=StudentSkill.SKILL_LEVELS,
        default="BEGINNER"
    )

    event_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

class Notification(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.user.username} - {self.title}"