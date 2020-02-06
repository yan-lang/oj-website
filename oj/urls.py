from django.urls import path

from . import views

app_name = 'oj'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assignment/', views.assignment, name='assignment')
]
