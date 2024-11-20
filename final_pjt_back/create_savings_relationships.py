import random
from django.contrib.auth import get_user_model
from savings.models import SavingProduct

User = get_user_model()

# 모든 사용자와 적금 상품을 가져옵니다
users = User.objects.all()
savings = SavingProduct.objects.all()

# 각 사용자에게 랜덤하게 1~5개의 적금 상품을 할당합니다
for user in users:
    num_savings = random.randint(1, 5)
    selected_savings = random.sample(list(savings), num_savings)
    user.owned_savings.add(*selected_savings)

print("사용자와 적금 상품 간의 관계가 성공적으로 생성되었습니다.")