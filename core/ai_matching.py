import requests


def ai_match_student(student_skills, opportunity_skills):
    """
    Uses Ollama to analyze how well a student's skills
    match an opportunity.
    """

    prompt = f"""
You are an AI student talent matching assistant.

Student skills:
{student_skills}

Opportunity required skills:
{opportunity_skills}

Analyze the match between the student and the opportunity.

Give:
1. Match percentage from 0 to 100
2. Matching skills
3. Missing skills
4. Short recommendation

Keep the answer simple and concise.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:1.5b",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "No AI response received.")

    except requests.exceptions.RequestException as e:
        return f"AI connection error: {e}"