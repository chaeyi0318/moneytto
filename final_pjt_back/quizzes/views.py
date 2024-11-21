# views.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Quiz
from .serializers import QuizSerializer, RandomQuizSerializer
from django.contrib.auth import get_user_model
import random

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_random_quiz(request):
    unsolved_quizzes = Quiz.objects.exclude(solved_users=request.user)
    
    if unsolved_quizzes.exists():
        quiz = random.choice(unsolved_quizzes)
        serializer = RandomQuizSerializer(quiz)
        return Response(serializer.data)
    else:
        return Response({'message': '모든 퀴즈를 완료했습니다!'}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def answer_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user_answer = request.data.get('answer')
    
    is_correct = user_answer == quiz.answer
    points_earned = 0
    
    if is_correct:
        points = quiz.difficulty * 10
        request.user.point += points
        request.user.save()
        points_earned = points
        
        quiz.solved_users.add(request.user)
    else:
        quiz.failed_users.add(request.user)
    
    return Response({
        'is_correct': is_correct,
        'points_earned': points_earned,
        'explanation': quiz.explanation
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_solved_quizzes(request):
    user = request.user
    solved_quizzes = Quiz.objects.filter(solved_users=user)
    failed_quizzes = Quiz.objects.filter(failed_users=user).exclude(solved_users=user)

    solved_serializer = QuizSerializer(solved_quizzes, many=True)
    failed_serializer = QuizSerializer(failed_quizzes, many=True)

    return Response({
        'solved_quizzes': solved_serializer.data,
        'failed_quizzes': failed_serializer.data
    })