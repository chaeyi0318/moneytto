# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)                                 # 아이디
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)   # 프로필이미지
    nickname = models.CharField(max_length=30)                                              # 닉네임
    birth_date = models.DateField(null=True, blank=True)                                    # 생년월일
    income = models.IntegerField(default=0)                                                 # 월 수입
    created_at = models.DateTimeField(auto_now_add=True)                                    # 가입일
    updated_at = models.DateTimeField(auto_now=True)                                        # 수정일
    assets = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)             # 보유자산
    point = models.IntegerField(default=0)                                                  # 포인트


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')  # 연결된 유저
    amount = models.IntegerField(default=0)  # 예산 금액
    year = models.IntegerField()  # 연도
    month = models.IntegerField()  # 월
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    updated_at = models.DateTimeField(auto_now=True)  # 수정일

    def __str__(self):
        return f"Budget for {self.user.username} ({self.year}-{self.month}): {self.amount}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')  # 연결된 유저
    amount = models.IntegerField(default=0)  # 소비 금액
    year = models.IntegerField()  # 연도
    month = models.IntegerField()  # 월
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    updated_at = models.DateTimeField(auto_now=True)  # 수정일

    def __str__(self):
        return f"Expense for {self.user.username} ({self.year}-{self.month}): {self.amount}"