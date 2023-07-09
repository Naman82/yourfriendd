from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import json
from django.core import serializers
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from drf_social_oauth2.authentication import SocialAuthentication   
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from social_django.models import UserSocialAuth
from yourfriendd.utils import send_response
from .serializers import AppointmentSerializer,SubscriptionSerializer,SubscriberSerializer
from authentication.models import Consultant
image_id = openapi.Parameter('id', openapi.IN_QUERY, description="Id of object to delete", type=openapi.TYPE_INTEGER)
from .models import *
from authentication.models import Patient
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from dateutil.relativedelta import relativedelta
# Create your views here.

def subscriptionCheck(user):
    try:
        subscribed_users = Subscriber.objects.filter(patient=user)
        for i in subscribed_users:
            if i.subscribed_till > date.today():
                return True
    except ObjectDoesNotExist:
        pass
    return False

class AppointmentView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[OAuth2Authentication,SocialAuthentication]

    def get(self,request):
        try:
            if request.user.is_anonymous:
                return send_response(result=False, message="Authentication required")
            user = User.objects.get(pk=request.user.pk)
            if user.user_type == 1:
                is_subscribed = subscriptionCheck(user)
                if is_subscribed == False:
                    return send_response(result=True, message="Patient has not subscribed")
                else:
                    if Appointment.objects.filter(patient=user).exists():
                        appointments = Appointment.objects.filter(patient=user)
                        serializer = AppointmentSerializer(appointments,many=True)
                        return send_response(result=True,data=serializer.data)
                    else:
                        return send_response(result=True,message="Appointment does not exist")
            if Appointment.objects.filter(doctor=user).exists():
                appointments = Appointment.objects.filter(doctor=user)
                #only not conducted appointments logic need to be written
                serializer=AppointmentSerializer(appointments,many=True)
                return send_response(result=True,data=serializer.data)
            else:
               return send_response(result=True, message="No Appointments available")
        except Exception as e:
            return send_response(result=False, message=str(e))

    def post(self,request):
        try:
            # doctor=User.objects.get(pk=request.data.get('doctor'))
            # appointment = Appointment(patient=request.user, doctor=doctor,meet_link=request.data.get('meet_link'),date=request.data.get('date'))
            # appointment.save()
            if request.user.is_anonymous:
                return send_response(result=False, message="Authentication required")
            user = User.objects.get(pk=request.user.pk)
            if user.user_type == 1:
                doctor=User.objects.get(pk=request.data.get('doctor'))
                appointment = Appointment(patient=request.user, doctor=doctor,meet_link=request.data.get('meet_link'),date=request.data.get('date'))
                appointment.save()
                return send_response(result=True, message="Appointment Created Successfully")
            else:
                return send_response(result=False, message="Consultant cannot create appointment")
        except Exception as e:
            return send_response(result=False, message=str(e))
        
    

class AppointmentEditView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[OAuth2Authentication,SocialAuthentication]

    def patch(self,request,pk):
        try:
            if request.user.is_anonymous:
                return send_response(result=False, message="Authentication required")

            if request.user.user_type == 2:
                appointment = Appointment.objects.get(pk=pk)
                serializer=AppointmentSerializer(appointment,data=request.data,partial=True)
                # print(serializer.data)
                if serializer.is_valid():
                    serializer.save()
                    return send_response(result=True, message="Appointment Updated Successfully")
                else:
                    print(serializer.errors)
                    return send_response(result=False, message="Something went wrong")
            else:
                return send_response(result=True, message="Appointment can be edited by consultant")
        except Exception as e:
            return send_response(result=False, message=str(e))
    
class SubscriptionView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[OAuth2Authentication,SocialAuthentication]

    def get(self,request):
        try:
            subscriptions = Subscription_Model.objects.all()
            serializer = SubscriptionSerializer(subscriptions,many=True)
            return send_response(result=True,data=serializer.data)
        except Exception as e:
            return send_response(result=False, message=str(e))

    # SUBSCRIPTION MODEL TO BE ADDED BY ADMIN

    # def post(self,request):
    #     try:
    #         subscription=Subscription_Model(title=request.data.get('title'),description=request.data.get('description'),pricing=request.data.get('pricing'),expires_in=request.data.get('expires_in'))
    #         subscriber = Subscriber(patient=request.user,subscription=subscription)
    #         subscription.save()
    #         subscriber.save()
    #         return send_response(result=True, message="Subscription Added Successfully")
    #     except Exception as e:
    #         return send_response(result=False, message=str(e))

@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="subscription buy",
    tags=["subscription"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'subscription':openapi.Schema(type=openapi.TYPE_INTEGER, description="Subscription model id"),
        }
    )
))
class SubscriptionBuyView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[OAuth2Authentication,SocialAuthentication]

    def post(self,request):
        try:
            user = User.objects.get(pk=request.user.pk)
            subscription=Subscription_Model.objects.get(pk=request.data.get('subscription'))
            subscription_model_time = subscription.expires_in
            subscription_time = date.today()+relativedelta(months=subscription_model_time)
            if user.user_type == 1:
                is_subscribed = subscriptionCheck(user)
                if is_subscribed == False:
                    if Subscriber.objects.filter(subscription=subscription).exists():
                        subscribed_pack = Subscriber.objects.get(subscription=subscription)
                        subscribed_pack.subscribed_till = subscription_time
                        subscribed_pack.save()
                        return send_response(result=True,message="Subscription pack created successfully")
                    else:
                        new_subscribed_pack = Subscriber(patient=request.user,subscription=subscription,subscribed_till=subscription_time)
                        new_subscribed_pack.save()
                        return send_response(result=True,message="Subscription pack created successfully")
                else:
                    return send_response(result=True,message="Subscription pack already active")
            pass
        except Exception as e:
           return send_response(result=False, message=str(e))

