from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [

    path('', views.home, name='home'),
    path('user-home/', views.user_home, name='user_home'),
    path('play/', views.play, name='play'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    #path(r'^submission-result/(?P<attempted_question_pk>\d+)/', views.submission_result, name='submission_result'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]