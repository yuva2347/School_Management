from django.urls import path
from accounts import views

urlpatterns = [
    path('login.html/', views.login_view, name='login'),
    path('admin_dashboard.html/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher_dashboard.html/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard.html/', views.student_dashboard, name='student_dashboard'),
]
