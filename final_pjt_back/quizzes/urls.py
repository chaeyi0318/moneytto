from django.urls import path
from . import views

app_name = 'quizzes'
urlpatterns = [
    path('random-quiz/', views.get_random_quiz, name='random-quiz'),
    path('answer-quiz/<int:quiz_id>/', views.answer_quiz, name='answer-quiz'),
    path('solved-quizzes/', views.get_solved_quizzes, name='solved-quizzes'),
]
