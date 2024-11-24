# Generated by Django 4.2.16 on 2024-11-24 02:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SavingAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SavingPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('months', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SavingProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=50)),
                ('product_name', models.CharField(max_length=100)),
                ('saving_method', models.CharField(max_length=20)),
                ('pre_tax_interest_rate', models.FloatField()),
                ('post_tax_interest_rate', models.FloatField()),
                ('max_preference_rate', models.FloatField()),
                ('eligibility', models.CharField(max_length=20)),
                ('interest_calculation_method', models.CharField(max_length=10)),
                ('inquiry_info', models.CharField(max_length=200)),
                ('comparison_disclosure_date', models.CharField(max_length=100)),
                ('department_contact', models.CharField(max_length=200)),
                ('preferential_conditions', models.TextField()),
                ('detailed_eligibility', models.TextField()),
                ('application_method', models.CharField(max_length=100)),
                ('post_maturity_interest_rate', models.TextField()),
                ('other_considerations', models.TextField()),
                ('product_link', models.URLField()),
                ('institution_type', models.CharField(max_length=10)),
                ('liked_by', models.ManyToManyField(blank=True, related_name='liked_savings', to=settings.AUTH_USER_MODEL)),
                ('owned_by', models.ManyToManyField(blank=True, related_name='owned_savings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavingInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_tax_interest', models.FloatField(null=True)),
                ('amount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='savings.savingamount')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='savings.savingperiod')),
                ('saving', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='savings.savingproduct')),
            ],
        ),
    ]
