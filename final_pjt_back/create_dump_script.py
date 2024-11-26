import os
import sys
import django
from django.core.management import call_command

# Django 설정 모듈 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt_back.settings")

# Django 설정 로드
django.setup()

# 표준 출력을 파일로 리다이렉트
sys.stdout = open('db.json', 'w', encoding='utf-8')

# dumpdata 명령 실행
call_command('dumpdata', exclude=['auth.permission', 'contenttypes'], indent=4)

# 파일 닫기
sys.stdout.close()