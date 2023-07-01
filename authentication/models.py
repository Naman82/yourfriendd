from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MaxValueValidator
import os, uuid
from .managers import UserManager
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    def get_update_filename(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('uploads/user/profile', filename)
    username = None
    USER_TYPE_CHOICES = [
        (0, 'Admin'),
        (1, 'Patient'),
        (2, 'Consultant'),
    ]
    email = models.EmailField(_('email address'), unique=True, null=True)
    email_verified = models.BooleanField(default=False)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=1)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    profile_pic = models.ImageField(upload_to=get_update_filename, default='uploads/user/profile/default_profile.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']
    object = UserManager()

    def __str__(self):
        return "{},{},{}".format(self.email, self.first_name, self.type_value)

    def gettype(self):
        return self.user_type

    @property
    def type_value(self):
        return dict(self.USER_TYPE_CHOICES)[self.user_type]

#Patient Model
class Patient(models.Model):
    GENDER_TYPE_CHOICES = [
        (0, 'Male'),
        (1, 'Female'),
        (2, 'Others'),
    ]
    user = models.OneToOneField(User, related_name="thepatient", on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length = 350, default = "patient")
    age = models.PositiveIntegerField(default = 00)
    gender = models.IntegerField(choices=GENDER_TYPE_CHOICES,default = 0)
    history = models.CharField(max_length = 500, default = "None")

    def __str__(self):
        return self.name

#Consultant Model
class Consultant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=250, default = "doctor")
    qualification = models.CharField(max_length = 100,null=True,blank=True)
    speciality = models.CharField(max_length = 300,null=True,blank=True)
    clinic = models.CharField(max_length = 300,null=True,blank=True)
    contact = models.PositiveBigIntegerField(null=True,blank=True)
    email = models.EmailField(max_length = 200,null=True,blank=True)
    bio = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name
    

    
    
    

    

    
