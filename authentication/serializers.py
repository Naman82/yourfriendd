from rest_framework import serializers
from .models import Patient, Consultant,User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patient
        fields="__all__"

class ConsultantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Consultant
        fields="__all__"