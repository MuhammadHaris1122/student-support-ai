from django.urls import path
from . import views

urlpatterns = [
    path('feedback/', views.submit_feedback, name='submit_feedback'),
    path('api/weekly-summary/', views.weekly_summary_api, name='weekly_summary_api'),
]