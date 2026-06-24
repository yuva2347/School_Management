from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Remove role field if you had one
    pass

class RoleMaster(models.Model):
    role_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # store hashed password
    role = models.CharField(max_length=50)       # e.g. 'admin', 'teacher', 'student'

    def __str__(self):
        return f"{self.username} ({self.role})"

class LoginDetails(models.Model):
    user = models.ForeignKey(RoleMaster, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} logged in at {self.login_time}"
