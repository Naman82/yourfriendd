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
# Create your views here.

class AppointmentView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[OAuth2Authentication,SocialAuthentication]

    def get(self,request):
        try:
            if request.user.is_anonymous:
                return send_response(result=False, message="Authentication required")
            user = User.objects.get(pk=request.user.pk)
            if user.user_type != 2:
                return send_response(result=False, message=" Consultant does not exist")
            if Appointment.objects.filter(doctor=user).exists():
                appointments = Appointment.objects.filter(doctor=user)
                serializer=AppointmentSerializer(appointments,many=True)
                return send_response(data=serializer.data)
            else:
               return send_response(result=False, message="Patient Profile does not exists")
        except Exception as e:
            return send_response(result=False, message=str(e))

    def post(self,request):
        try:
            doctor=User.objects.get(pk=request.data.get('doctor'))
            appointment = Appointment(patient=request.user, doctor=doctor,meet_link=request.data.get('meet_link'),date=request.data.get('date'))
            appointment.save()
            return send_response(result=True, message="Appointment Created Successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))


class AppointmentEditView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[OAuth2Authentication,SocialAuthentication]

    def patch(self,request,pk):
        try:
            if request.user.is_anonymous:
                return send_response(result=False, message="Authentication required")
            # user=User.objects.get(pk=request.user.pk)
            # consultant=Consultant.objects.get(user=user)

            # if user.user_type != 2:
                # return send_response(result=False, message="Consultant does not exist")
            appointment = Appointment.objects.get(pk=pk)

            serializer=AppointmentSerializer(appointment,data=request.data,partial=True)
            # print(serializer.data)
            if serializer.is_valid():
                serializer.save()
                return send_response(result=True, message="Appointment Updated Successfully")
            else:
                print(serializer.errors)
                return send_response(result=False, message="Something went wrong")
        except Exception as e:
            return send_response(result=False, message=str(e))
    
class SubscriptionView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[OAuth2Authentication,SocialAuthentication]

    def post(self,request):
        try:
            subscription=Subscription_Model(title=request.data.get('title'),description=request.data.get('description'),pricing=request.data.get('pricing'),expires_in=request.data.get('expires_in'))
            subscriber = Subscriber(patient=request.user,subscription=subscription)
            subscription.save()
            subscriber.save()
            return send_response(result=True, message="Subscription Added Successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))

# class SelfCareView(APIView):
#     parser_classes=[MultiPartParser,FormParser]
#     permission_classes=[IsAuthenticated]
#     authentication_classes=[OAuth2Authentication,SocialAuthentication]

#     def get(self,request):
#         try:
#             if request.user.is_anonymous:
#                 return send_response(result=False, message="Authentication required")

#             techniques= Self_Care.objects.all()
#             serializer=SelfCareSerializer(techniques,many=True)
#             return send_response(data=serializer.data)
#         except Exception as e:
#             return send_response(result=False, message=str(e))

#     def post(self,request):
#         try:
#             if request.user.is_anonymous:
#                 return send_response(result=False, message="Authentication required")
#             user = User.objects.get(pk=request.user.pk)
#             if user.user_type != 2:
#                 return send_response(result=False, message=" Consultant does not exist")
#             selfcare=Self_Care(title=request.data.get('title'),posted_by=request.user,file=request.data.get('file'))
#             selfcare.save()
#             # serializer=SelfCareSerializer(data=request.data)
#             # if serializer.is_valid():
#             #     serializer.save()
#             return send_response(result=True, message="Self Care Techniques Added Successfully")
#             # else:
#             #     return send_response(result=False, message="Something went wrong")
#         except Exception as e:
#             return send_response(result=False, message=str(e))

#     def patch(self,request):
#         try:
#             if request.user.is_anonymous:
#                 return send_response(result=False, message="Authentication required")
#             consultant=User.objects.get(pk=request.user.pk)
#             if consultant.user_type != 2:
#                 return send_response(result=False, message=" Consultant does not exist")
#             serializer=SelfCareSerializer(posted_by=consultant,data=request.data,partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return send_response(result=True, message="Self Care Technique Updated Successfully")
#             else:
#                 return send_response(result=False, message="Something went wrong")
#         except Exception as e:
#             return send_response(result=False, message=str(e))

# class SelfCareEditView(APIView):
    # parser_classes=[MultiPartParser,FormParser]
    # permission_classes=[IsAuthenticated]
    # authentication_classes=[OAuth2Authentication,SocialAuthentication]

    # def patch(self,request,pk):
    #     try:
    #         selfcare=Self_Care.objects.get(pk=pk)

    #         serializer=SelfCareSerializer(selfcare,data=request.data,partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return send_response(result=True, message="Self Care Technique Updated Successfully")
    #         else:
    #             print(serializer.data)
    #             return send_response(result=False, message="Something went wrong")
    #     except Exception as e:
    #         return send_response(result=False, message=str(e))