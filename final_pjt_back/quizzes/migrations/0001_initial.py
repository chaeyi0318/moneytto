# Generated by Django 4.2.16 on 2024-11-24 02:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300)),
                ('answer', models.CharField(max_length=10)),
                ('explanation', models.TextField()),
                ('difficulty', models.IntegerField()),
                ('failed_users', models.ManyToManyField(blank=True, related_name='failed_quizzes', to=settings.AUTH_USER_MODEL)),
                ('solved_users', models.ManyToManyField(blank=True, related_name='solved_quizzes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
