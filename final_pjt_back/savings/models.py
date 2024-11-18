from django.db import models

# Create your models here.

# 적금상품
class SavingProduct(models.Model):
    bank_name = models.CharField(max_length=50, null=False)         # 금융회사
    product_name = models.CharField(max_length=100)                 # 상품명
    saving_method = models.CharField(max_length=20)                 # 적립방식(정액적립식/자유적립식)
    pre_tax_interest_rate = models.FloatField()                     # 세전이자율
    post_tax_interest_rate = models.FloatField()                    # 세후이자율
    max_preference_rate = models.FloatField()                       # 최고우대금리
    eligibility = models.CharField(max_length=20)                   # 가입대상(제한없음/../ )
    interest_calculation_method = models.CharField(max_length=10)   # 이자계산방식(단리/복리)
    inquiry_info = models.CharField(max_length=200)                 # 금융상품문의
    comparison_disclosure_date = models.CharField(max_length=100)   # 비교공시일
    department_contact = models.CharField(max_length=200)           # 담당부서 및 연락처
    preferential_conditions = models.TextField()                    # 우대조건
    detailed_eligibility = models.TextField()                       # 상세 가입대상
    application_method = models.CharField(max_length=100)           # 가입방법
    post_maturity_interest_rate = models.TextField()                # 만기 후 이자율
    other_considerations = models.TextField()                       # 기타 유의사항
    product_link = models.URLField()                                # 상품 링크
    institution_type = models.CharField(max_length=10)              # 금융권역(은행/저축은행/신협조합)
    
    def __str__(self):
        return f"{self.bank_name} - {self.product_name} - {self.saving_method}"

# 납입 기간
class SavingPeriod(models.Model):
    months = models.IntegerField()
    
    def __str__(self):
        return f"{self.months}개월"

# 월 납입 금액
class SavingAmount(models.Model):
    amount = models.IntegerField()
    
    def __str__(self):
        return f"월 납입금액 {self.amount}원"
    
class SavingInterest(models.Model):
    saving = models.ForeignKey(SavingProduct, on_delete=models.CASCADE)
    period = models.ForeignKey(SavingPeriod, on_delete=models.CASCADE)
    amount = models.ForeignKey(SavingAmount, on_delete=models.CASCADE)
    post_tax_interest = models.FloatField(null=True)
    
    def __str__(self):
        return f"{self.saving.product_name} - {self.period.months}개월 {self.amount.amount}원 적금 시 세후 {self.post_tax_interest} 수령"
    