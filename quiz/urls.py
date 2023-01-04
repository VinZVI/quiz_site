from django.urls import path

from . import views

app_name = 'quiz'

urlpatterns = [

    path('', views.home, name='home'),
    path('choose_of_quizzes/', views.choose_of_quizzes, name='choose_of_quizzes'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.quiz_detail, name='quiz_detail'),
    path('play/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.play, name='play'),
    path('leaderboard/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.leaderboard, name='leaderboard'),
    path('submission-result/<int:attempted_question_pk>/', views.submission_result, name='submission_result'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]
