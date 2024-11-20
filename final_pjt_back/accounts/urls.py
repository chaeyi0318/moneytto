from django.urls import path
from . import views
from .views import CustomRegisterView, UserAdditionalInfoView

urlpatterns = [
    path('signup/', CustomRegisterView.as_view()),
    path('login/', views.login),
    path('logout/', views.logout),
    path('additional-info/', UserAdditionalInfoView.as_view(), name='user-additional-info'),
    path('update/', views.update_user, name='update-user'),
    path('delete/', views.delete_user, name='delete-user'),
]