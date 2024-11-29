from django.urls import path
from . import views

app_name = 'savings'
urlpatterns = [
    path('search/', views.search_savings),
    path('likes/<int:saving_pk>/', views.likes),
    path('owns/<int:saving_pk>/', views.owns),
    path('recommend/', views.recommend_savings),
    path('liked-savings/', views.liked_savings, name='liked-savings'),

]
