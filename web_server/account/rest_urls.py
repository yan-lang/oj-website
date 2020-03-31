from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('students', views.StudentViewset)

urlpatterns = [
    path('', include(router.urls))
]
