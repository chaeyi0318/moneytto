from django.urls import path
from . import views
from .views import CustomRegisterView, UserAdditionalInfoView

urlpatterns = [
    path('signup/', CustomRegisterView.as_view()),
    path('login/', views.login),
    path('logout/', views.logout),
    path('additional-info/', views.add_info),
    path('update/', views.update_user),
    path('delete/', views.delete_user,),
    path('update-budget/', views.update_budget),
    # path('profile/<str:username>/', views.profile),
]