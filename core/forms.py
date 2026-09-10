from django import forms
from django.contrib.auth.models import User
from .models import ( StudentSkill, Profile, StudentProject, StudentCertification, 
                     Opportunity, )


class StudentSkillForm(forms.ModelForm):

    class Meta:
        model = StudentSkill
        fields = [
            "skill_name",
            "skill_level",
            "years_experience",
        ]

        widgets = {
            "skill_name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Python, Django, React"
                }
            ),

            "skill_level": forms.Select(),

            "years_experience": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 1.5",
                    "step": "0.1",
                    "min": "0"
                }
            ),
        }

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            "department",
            "phone",
            "year",
        ]

        widgets = {
            "department": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Artificial Intelligence and Data Science"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Enter phone number"
                }
            ),

            "year": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 3",
                    "min": "1",
                    "max": "6"
                }
            ),
        }

class StudentProjectForm(forms.ModelForm):

    class Meta:
        model = StudentProject

        fields = [
            "project_title",
            "description",
            "technologies",
            "project_type",
        ]

        widgets = {
            "project_title": forms.TextInput(
                attrs={
                    "placeholder": "e.g. BloodBridge AI"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "placeholder": "Describe what you built...",
                    "rows": 4
                }
            ),

            "technologies": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Python, Django, Machine Learning"
                }
            ),

            "project_type": forms.TextInput(
                attrs={
                    "placeholder": "e.g. AI/ML, Web, Mobile"
                }
            ),
        }


class StudentCertificationForm(forms.ModelForm):

    class Meta:
        model = StudentCertification

        fields = [
            "certificate_name",
            "issuing_organization",
            "issue_year",
        ]

        widgets = {
            "certificate_name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Python Programming"
                }
            ),

            "issuing_organization": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Coursera, Google, Microsoft"
                }
            ),

            "issue_year": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 2026",
                    "min": "2000",
                    "max": "2100"
                }
            ),
        }

class OpportunityForm(forms.ModelForm):

    class Meta:
        model = Opportunity

        fields = [
            "title",
            "description",
            "opportunity_type",
            "required_skills",
            "minimum_skill_level",
            "event_date",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "e.g. AI Innovation Hackathon"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "placeholder": "Describe the opportunity...",
                    "rows": 4
                }
            ),

            "required_skills": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Python, Machine Learning, Django"
                }
            ),

            "event_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
        }


class StudentRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Create password"
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm password"
            }
        )
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Choose a username"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Enter your email"
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data