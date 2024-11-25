import os
import django
import random
from datetime import datetime, timedelta
import sys

# Django 설정 파일 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt_back.settings")
django.setup()

from django.contrib.auth import get_user_model
from savings.models import SavingProduct

# UTF-8 인코딩 설정
sys.stdout.reconfigure(encoding='utf-8')

User = get_user_model()

# 더미 사용자 데이터 생성
def create_dummy_users():
    for i in range(1, 501):
        username = f'user_{i}'
        nickname = f'닉네임_{i}'
        birth_date = datetime.now() - timedelta(days=random.randint(12*365, 70*365))
        income = random.randint(0, 20000000)
        assets = round(random.uniform(0, 100000000), 2)
        point = random.randint(0, 1000)
        
        User.objects.create_user(
            username=username,
            password='user1234',  # 보안을 위해 실제 사용 시 변경 필요
            profile_image=None,
            nickname=nickname,
            birth_date=birth_date.date(),
            income=income,
            assets=assets,
            point=point
        )
    print("500명의 더미 사용자 데이터가 성공적으로 생성되었습니다.")

# 사용자와 적금 상품 간의 관계 생성
def create_savings_relationships():
    users = User.objects.all()
    savings = SavingProduct.objects.all()

    for user in users:
        num_savings = random.randint(1, 5)
        selected_savings = random.sample(list(savings), num_savings)
        user.owned_savings.add(*selected_savings)
    
    print("사용자와 적금 상품 간의 관계가 성공적으로 생성되었습니다.")

if __name__ == "__main__":
    create_dummy_users()
    create_savings_relationships()

    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write("더미 사용자 데이터 생성 및 적금 상품 관계 설정이 완료되었습니다.")