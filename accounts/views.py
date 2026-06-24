from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from accounts.models import User, RoleMaster, LoginDetails
from teachers.models import Teacher
from students.models import Student
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as DjangoUser



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            role_entry = RoleMaster.objects.get(username=username)

            if role_entry.password == password or check_password(password, role_entry.password):
                try:
                    user = User.objects.get(username=username)
                    if not user.check_password(password):
                        user.set_password(password)
                        user.save()
                except User.DoesNotExist:
                    user = User.objects.create_user(username=username, password=password)

                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)

                # Redirect based on role
                if role_entry.role == 'admin':
                    return redirect('admin_dashboard')
                elif role_entry.role == 'teacher':
                    return redirect('teacher_dashboard')
                elif role_entry.role == 'student':
                    return redirect('student_dashboard')
                else:
                    return render(request, 'accounts/login.html', {'error': 'Unknown role'})
            else:
                return render(request, 'accounts/login.html', {'error': 'Invalid password'})
        except RoleMaster.DoesNotExist:
            return render(request, 'accounts/login.html', {'error': 'User not found'})

    return render(request, 'accounts/login.html')


@login_required
def admin_dashboard(request):
    try:
        role_entry = RoleMaster.objects.get(username=request.user.username)
    except RoleMaster.DoesNotExist:
        return redirect('login')

    if role_entry.role != 'admin':
        return redirect('login')

    teachers = Teacher.objects.all()
    students = Student.objects.all()
    return render(request, 'accounts/admin_dashboard.html', {
        'teachers': teachers,
        'students': students
    })


@login_required
def teacher_dashboard(request):
    try:
        role_entry = RoleMaster.objects.get(username=request.user.username)
    except RoleMaster.DoesNotExist:
        return redirect('login')

    if role_entry.role != 'teacher':
        return redirect('login')

    teacher_profile = Teacher.objects.get(user=request.user)
    students = Student.objects.filter(assigned_teacher=teacher_profile)
    return render(request, 'accounts/teacher_dashboard.html', {
        'students': students
    })


@login_required
def student_dashboard(request):
    try:
        role_entry = RoleMaster.objects.get(username=request.user.username)
    except RoleMaster.DoesNotExist:
        return redirect('login')

    if role_entry.role != 'student':
        return redirect('login')

    student = Student.objects.get(user=request.user)
    return render(request, 'accounts/student_dashboard.html', {
        'student': student
    })
