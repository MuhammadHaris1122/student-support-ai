from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('api/ask/', views.ask_question_api, name='ask_question_api'),
]