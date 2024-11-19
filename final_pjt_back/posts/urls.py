from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('create-post/', views.create_post),
    path('detail-post/<int:post_pk>/', views.detail_post)
]
