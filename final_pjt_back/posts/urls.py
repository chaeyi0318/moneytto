from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('create-post/', views.create_post),
    path('detail-post/', views.detail_post),
    path('post-list/', views.post_list,),
    path('delete-post/<int:post_id>/', views.delete_post,),
    path('create-comment/', views.create_comment),
    path('comment-list/', views.comment_list),
    path('delete-comment/<int:comment_id>/',views.delete_comment),
    path('update-comment/<int:comment_id>/', views.update_comment),
]