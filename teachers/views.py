from django.shortcuts import render, redirect, get_object_or_404
from .models import Teacher
from .forms import TeacherForm

def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = TeacherForm()
    return render(request, 'teachers/add_teacher.html', {'form': form})

def edit_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'teachers/edit_teacher.html', {'form': form})

def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.delete()
    return redirect('admin_dashboard')
from students.models import Student
from students.forms import UpdateMarksForm

def update_marks(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = UpdateMarksForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = UpdateMarksForm(instance=student)
    return render(request, 'teachers/update_marks.html', {'form': form, 'student': student})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student
from teachers.models import Teacher

@login_required
def teacher_dashboard(request):
    teacher = Teacher.objects.get(user=request.user)
    students = Student.objects.filter(assigned_teacher=teacher)
    return render(request, 'teachers/teacher_dashboard.html', {
        'students': students
    })
