from django.contrib import admin
from .models import User, Patient, Consultant
# Register your models here.

admin.site.register((User, Patient, Consultant))
