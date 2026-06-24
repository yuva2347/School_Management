from django import forms
from django.contrib.auth.hashers import make_password

from accounts.models import RoleMaster, User
from teachers.models import Teacher
from .models import Student


class StudentForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['student_id', 'grade', 'marks', 'email', 'assigned_teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_teacher'].queryset = Teacher.objects.all().order_by('teacher_id')
        self.fields['assigned_teacher'].label = 'Assign Teacher'
        self.fields['assigned_teacher'].help_text = 'Choose the teacher who will manage this student.'
        self.fields['assigned_teacher'].empty_label = 'Select a teacher'

    def save(self, commit=True):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user, created = User.objects.get_or_create(username=username)
        if created or not user.check_password(password):
            user.set_password(password)
            user.save()

        RoleMaster.objects.update_or_create(
            username=username,
            defaults={'password': make_password(password), 'role': 'student'}
        )

        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student


class UpdateMarksForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['grade', 'marks']
