from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from django.core.exceptions import ValidationError
# Create your models here.
import os
def get_user_path(instance, filename): 
    ext = filename.split('.')[1]
    "/profile/arjunmbt.ext"
    path = os.path.join("/profile/", instance.username+'.'+ext)
    return path 
   
class User(AbstractBaseUser):
    profile_pic = models.ImageField(unique=True, upload_to=get_user_path, default="/profile/default.jpg")
    email = models.EmailField(unique=True, max_length=100, null=False, default="username@gmail.com")
    username = models.CharField(unique=True, max_length = 50, null=False, default="John Doe")
    REQUIRED_FIELDS = ['email', 'username']

def get_project_path(instance, filename): 
    ext = filename.split('.')[1]
    path = os.path.join("/project/", instance.name+'.'+ext)
    return path 

status_list = ['started', 'In Progress', 'Completed'] 
 
class Project(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(null=False, unique=True, max_length=100)
    desc = models.CharField(null=True, max_length=255)
    icon = models.ImageField(unique=True, upload_to=get_project_path, default="/project/default.jpg")
    members = models.ManyToManyField(User, related_name="members", blank=True, db_index=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=False)
    completed = models.BooleanField(default=False)
    status = models.CharField(max_length=50)

    def clean_status(self):
        value = self.status
        if value not in self.status_list:
            raise ValidationError({'detail': f'Invalid value. Only {self.MY_CHOICES} are allowed.'})
        
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)
    name = models.CharField(null=False, unique=True, max_length=100)
    desc = models.CharField(null=True, max_length=255)
    status = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=False)
    completed = models.BooleanField(default=False)
    def clean_status(self):
        value = self.status
        if value not in self.status_list:
            raise ValidationError({'detail': f'Invalid value. Only {self.MY_CHOICES} are allowed.'})