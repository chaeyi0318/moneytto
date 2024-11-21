from django.db import models
from django.conf import settings

# Create your models here.
class Quiz(models.Model):
    question = models.CharField(max_length=300)     # 문제
    answer = models.CharField(max_length=10)        # 답
    explanation = models.TextField()                # 설명
    difficulty = models.IntegerField()              # 난이도 (1, 2, 3)
    solved_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='solved_quizzes', blank=True)      # 맞힌 유저 / 역참조로 유저 측에서 맞힌 문제 접근할 수 있도록
    failed_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='failed_quizzes', blank=True)      # 틀린 유저