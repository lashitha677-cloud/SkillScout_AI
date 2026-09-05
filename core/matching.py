from .models import StudentSkill


SKILL_LEVELS = {
    "BEGINNER": 1,
    "INTERMEDIATE": 2,
    "ADVANCED": 3,
    "EXPERT": 4,
}


def check_student_eligibility(profile, opportunity):

    # Get required skills from the opportunity
    required_skills = list(dict.fromkeys(
        skill.strip().lower()
        for skill in opportunity.required_skills.split(",")
        if skill.strip()
    ))

    # Get all skills belonging to this student
    student_skill_records = StudentSkill.objects.filter(
        profile=profile
    )

    # Store the HIGHEST level for each skill
    student_skills = {}

    for skill in student_skill_records:

        skill_name = skill.skill_name.strip().lower()

        student_level = SKILL_LEVELS.get(
            skill.skill_level,
            1
        )

        # Keep the highest level if the student has
        # the same skill more than once
        if (
            skill_name not in student_skills
            or student_level > student_skills[skill_name]["level"]
        ):
            student_skills[skill_name] = {
                "skill": skill,
                "level": student_level,
            }

    matched_skills = []
    missing_skills = []

    # Required minimum level
    required_level = SKILL_LEVELS.get(
        opportunity.minimum_skill_level,
        1
    )

    # Check every required skill
    for required_skill in required_skills:

        student_skill = student_skills.get(
            required_skill
        )

        if student_skill:

            student_level = student_skill["level"]

            if student_level >= required_level:

                matched_skills.append(
                    required_skill
                )

            else:

                missing_skills.append(
                    required_skill
                )

        else:

            missing_skills.append(
                required_skill
            )

    # Calculate percentage
    total_required = len(required_skills)

    if total_required == 0:

        match_percentage = 0

    else:

        match_percentage = round(
            (
                len(matched_skills)
                / total_required
            ) * 100
        )

    # Student is eligible only when
    # every required skill meets the level
    eligible = (
        total_required > 0
        and len(missing_skills) == 0
    )

    return {
    "eligible": eligible,
    "match_percentage": match_percentage,
    "matched_skills": matched_skills,
    "missing_skills": missing_skills,

    "recommendation": (
        "Strong candidate for this opportunity."
        if match_percentage >= 80
        else
        "Good candidate, but some skills need improvement."
        if match_percentage >= 50
        else
        "Not currently recommended for this opportunity."
    ),
}