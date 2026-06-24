from django import forms
from django.contrib.auth.hashers import make_password
from .models import Teacher
from accounts.models import User, RoleMaster

class TeacherForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Teacher
        fields = ['teacher_id', 'subject', 'email']

    def save(self, commit=True):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
        elif not user.check_password(password):
            user.set_password(password)
            user.save()

        RoleMaster.objects.update_or_create(
            username=username,
            defaults={'password': make_password(password), 'role': 'teacher'}
        )

        teacher = super().save(commit=False)
        teacher.user = user
        if commit:
            teacher.save()
        return teacher
