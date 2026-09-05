import requests


def ask_qwen(prompt):

    url = "http://127.0.0.1:11434/api/generate"

    data = {
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 150
        }
    }

    try:

        response = requests.post(
            url,
            json=data,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        return result.get(
            "response",
            "Scout could not generate a response."
        )

    except requests.exceptions.Timeout:

        return "Scout is taking too long to respond. Please try again."

    except requests.exceptions.RequestException:

        return "AI service is currently unavailable."