from django.urls import path

from . import views

app_name = 'settings'

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('account/', views.account, name='account')
]

