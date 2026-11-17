from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import StudentFeedback, StudentProgress
from assistant.models import ChatMessage

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        difficult_topic = request.POST.get('difficult_topic', '')
        comments = request.POST.get('comments', '')

        StudentFeedback.objects.create(
            student=request.user,
            rating=rating,
            difficult_topic=difficult_topic,
            comments=comments
        )
        return redirect('chat')
    return render(request, 'analytics/feedback.html')

def weekly_summary_api(request):
    """Endpoint for n8n / Make.com automation."""
    total_students = StudentProgress.objects.count()
    total_queries = ChatMessage.objects.count()
    feedbacks = list(StudentFeedback.objects.values('student__username', 'rating', 'difficult_topic', 'comments')[:10])

    data = {
        'total_active_students': total_students,
        'total_questions_asked': total_queries,
        'recent_feedbacks': feedbacks
    }
    return JsonResponse(data)