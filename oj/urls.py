from django.urls import path

from . import views

app_name = 'oj'

urlpatterns = [
    path('index/', views.index, name='index'),
]

urlpatterns += [
    path('courses/', views.CourseListview.as_view(), name='course_list'),
    path('courses/<slug:course_identifier>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<slug:course_identifier>/assignments/<int:pk>/', views.CourseAssignmentView.as_view(),
         name='course_assignment'),
]
