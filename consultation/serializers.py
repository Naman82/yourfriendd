from rest_framework import serializers
from .models import Appointment, Subscriber, Subscription_Model

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Appointment
        fields="__all__"

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subscriber
        fields="__all__"

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subscription_Model
        fields="__all__"