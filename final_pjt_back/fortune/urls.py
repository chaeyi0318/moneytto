from django.urls import path
from . import views

app_name = 'fortune'

urlpatterns = [
    path('chatbot/', views.chat_with_openai)
]
