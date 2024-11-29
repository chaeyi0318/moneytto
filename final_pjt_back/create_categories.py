import os
import django

# Django 설정 파일 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt_back.settings")
django.setup()

from posts.models import Category  # your_app_name을 실제 앱 이름으로 변경하세요

# 추가할 카테고리 리스트
categories = [
    "주거", "통신", "식비", "생활용품", "의복", "미용", "건강", "문화",
    "교육", "교통", "차량", "경조사", "회비", "세금", "용돈", "기타"
]

# 카테고리 생성 및 저장
for category_name in categories:
    Category.objects.get_or_create(category_name=category_name)

print(f"{len(categories)}개의 카테고리가 성공적으로 생성되었습니다.")