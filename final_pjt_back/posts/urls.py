from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('create-post/', views.create_post),
    path('detail-post/<str:date>/', views.detail_post),
    path('post-list/', views.post_list,)
]