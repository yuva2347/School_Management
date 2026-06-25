from django.conf import settings
from django.db import models

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=20, unique=True)
    subject = models.CharField(max_length=100)
    email = models.EmailField()
    qualification = models.CharField(max_length=200, blank=True)
    experience = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.teacher_id} - {self.user.username}" if self.user else self.teacher_id
