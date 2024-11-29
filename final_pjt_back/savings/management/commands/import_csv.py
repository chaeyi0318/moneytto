import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from savings.models import SavingProduct, SavingPeriod, SavingAmount, SavingInterest

class Command(BaseCommand):
    help = 'Import CSV data into the database'

    def handle(self, *args, **options):
        self.import_saving_products()
        self.import_saving_periods()
        self.import_saving_amounts()
        self.import_saving_interests()

    def import_saving_products(self):
        file_path = os.path.join(settings.BASE_DIR, 'savings', 'data', 'savings_products.csv')
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                SavingProduct.objects.create(
                    bank_name=row['company'],
                    product_name=row['product_name'],
                    saving_method=row['saving_method'],
                    pre_tax_interest_rate=float(row['pre_tax_interest_rate']),
                    post_tax_interest_rate=float(row['post_tax_interest_rate']),
                    max_preference_rate=float(row['max_preference_rate']),
                    eligibility=row['eligibility'],
                    interest_calculation_method=row['interest_calculation_method'],
                    inquiry_info=row['inquiry_info'],
                    comparison_disclosure_date=row['comparison_disclosure_date'],
                    department_contact=row['department_contact'],
                    preferential_conditions=row['preferential_conditions'],
                    detailed_eligibility=row['detailed_eligibility'],
                    application_method=row['application_method'],
                    post_maturity_interest_rate=row['post_maturity_interest_rate'],
                    other_considerations=row['other_considerations'],
                    product_link=row['product_link'],
                    institution_type=row['institution_type']
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported savings products'))

    def import_saving_periods(self):
        file_path = os.path.join(settings.BASE_DIR, 'savings', 'data', 'savings_periods.csv')
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                SavingPeriod.objects.create(months=int(row['months']))
        self.stdout.write(self.style.SUCCESS('Successfully imported saving periods'))

    def import_saving_amounts(self):
        file_path = os.path.join(settings.BASE_DIR, 'savings', 'data', 'monthly_payments.csv')
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                SavingAmount.objects.create(amount=int(row['amount']))
        self.stdout.write(self.style.SUCCESS('Successfully imported saving amounts'))

    def import_saving_interests(self):
        file_path = os.path.join(settings.BASE_DIR, 'savings', 'data', 'post_tax_interest.csv')
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                SavingInterest.objects.create(
                    saving_id=int(row['savings_product_id']),
                    period_id=int(row['savings_period_id']),
                    amount_id=int(row['monthly_payment_id']),
                    post_tax_interest=float(row['post_tax_interest']) if row['post_tax_interest'] else None
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported saving interests'))
