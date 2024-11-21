from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('create-post/', views.create_post),
    path('detail-post/', views.detail_post),
    path('post-list/', views.post_list,),
    path('create-comment/', views.create_comment),
]