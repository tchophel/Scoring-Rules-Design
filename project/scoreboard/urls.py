from django.urls import path
from . import views

urlpatterns = [
    path('', views.leaderboard, name='leaderboard'),
    path('matches/', views.matches, name='matches'),
    path('my-predictions/', views.my_predictions, name='my_predictions'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
