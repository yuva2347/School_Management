
from django.conf import settings
from django.db import models
from teachers.models import Teacher

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    grade = models.CharField(max_length=10)
    marks = models.IntegerField(default=0)
    email = models.EmailField()
    assigned_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )

    def __str__(self):
        return self.user.username
