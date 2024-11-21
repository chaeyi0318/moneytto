import pandas as pd
from django.core.management.base import BaseCommand
from quizzes.models import Quiz  # quiz는 해당 앱 이름으로 변경

class Command(BaseCommand):
    help = '금융 퀴즈 데이터를 데이터베이스에 저장합니다.'

    def handle(self, *args, **options):
        # CSV 파일 읽기
        df = pd.read_csv('quiz.csv')
        
        # 데이터 삽입
        for _, row in df.iterrows():
            Quiz.objects.get_or_create(
                question=row['question'],
                answer=row['answer'],
                explanation=row['explanation'],
                difficulty=row['difficulty']
            )
        
        self.stdout.write(self.style.SUCCESS('퀴즈 데이터 저장 완료!'))