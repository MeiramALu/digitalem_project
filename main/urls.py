from django.urls import path
from . import views
from .views import send_telegram_message

urlpatterns = [
    path('', views.index, name='index'),
    path('labs/', views.labs, name='labs'),

    path('projects/<slug:category_slug>/', views.project_list, name='project_list'),
    path('projects/details/<slug:slug>/', views.project_detail, name='project_detail'),

    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),

    path('team/', views.team_list, name='team_list'),
    path('team/<slug:slug>/', views.team_member_detail, name='team_member_detail'),
    path('send-telegram/', send_telegram_message, name='send_telegram'),
]