from django.urls import path
from . import views
from .views import CustomRegisterView

urlpatterns = [
    path('signup/', CustomRegisterView.as_view()),
    path('login/', views.login),
    path('logout/', views.logout),
]