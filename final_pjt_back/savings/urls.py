from django.urls import path
from . import views

app_name = 'savings'
urlpatterns = [
    path('search/', views.search_savings),
]
