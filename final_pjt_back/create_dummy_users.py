import os
import django
import random
from datetime import datetime, timedelta

# Django 설정 파일 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# 더미 데이터 생성 및 저장
for i in range(1, 501):
    username = f'user_{i}'
    nickname = f'닉네임_{i}'
    birth_date = datetime.now() - timedelta(days=random.randint(19*365, 99*365))
    income = random.randint(2000000, 10000000)
    assets = round(random.uniform(0, 100000000), 2)
    point = random.randint(0, 1000)
    
    User.objects.create_user(
        username=username,
        password='user1234',  # 보안을 위해 실제 사용 시 변경 필요
        profile_image=f'https://example.com/image_{i}.jpg',
        nickname=nickname,
        birth_date=birth_date.date(),
        income=income,
        assets=assets,
        point=point
    )

print("500명의 더미 사용자 데이터가 성공적으로 생성되었습니다.")