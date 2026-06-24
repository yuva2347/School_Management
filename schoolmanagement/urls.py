from django.contrib import admin
from django.urls import path
from accounts import views as account_views
from teachers import views as teacher_views
from students import views as student_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_views.login_view, name='login'),

    # Dashboards
    path('admin_dashboard/', account_views.admin_dashboard, name='admin_dashboard'),
    path('teacher_dashboard/', account_views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', account_views.student_dashboard, name='student_dashboard'),

    path('add_teacher/', teacher_views.add_teacher, name='add_teacher'),
    path('edit_teacher/<int:pk>/', teacher_views.edit_teacher, name='edit_teacher'),
    path('delete_teacher/<int:pk>/', teacher_views.delete_teacher, name='delete_teacher'),

    path('add_student/', student_views.add_student, name='add_student'),
    path('edit_student/<int:pk>/', student_views.edit_student, name='edit_student'),
    path('delete_student/<int:pk>/', student_views.delete_student, name='delete_student'),

    path('update_marks/<int:pk>/', teacher_views.update_marks, name='update_marks'),

]


