from django.shortcuts import render
from django.http import JsonResponse
from .ai import ask_qwen


def ai_assistant(request):

    if request.method == "POST":

        question = request.POST.get("question", "").strip()

        if not question:
            return JsonResponse({
                "error": "Please enter a question."
            }, status=400)

        # Get AI answer
        response = ask_qwen(question)

        # Get existing chat history
        chat_history = request.session.get("scout_chat", [])

        # Add new chat
        chat_history.append({
            "question": question,
            "response": response,
        })

        # Save chat history
        request.session["scout_chat"] = chat_history
        request.session.modified = True

        return JsonResponse({
            "question": question,
            "response": response,
        })

    # Normal page opening
    chat_history = request.session.get("scout_chat", [])

    return render(
        request,
        "ai/assistant.html",
        {
            "chat_history": chat_history,
        }
    )