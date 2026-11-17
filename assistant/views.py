from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from .rag_service import query_rag
from analytics.models import StudentProgress

@login_required
def chat_view(request):
    """Renders student chat interface."""
    return render(request, 'assistant/chat.html')

@login_required
def ask_question_api(request):
    """Asynchronous endpoint for RAG chat."""
    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        if not question:
            return JsonResponse({'error': 'Question cannot be empty'}, status=400)

        # Call RAG Pipeline
        answer = query_rag(question)

        # Save to DB
        ChatMessage.objects.create(
            user=request.user,
            question=question,
            answer=answer
        )

        # Update Student Analytics
        progress, _ = StudentProgress.objects.get_or_create(student=request.user)
        progress.questions_asked += 1
        progress.save()

        return JsonResponse({'question': question, 'answer': answer})

    return JsonResponse({'error': 'Invalid request method'}, status=405)