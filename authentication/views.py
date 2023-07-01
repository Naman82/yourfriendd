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
from .serializers import PatientProfileSerializer,ConsultantProfileSerializer,UserSerializer
from drf_social_oauth2.views import TokenView, ConvertTokenView
from django.conf import settings
from rest_framework.response import Response
from django.http import JsonResponse
image_id = openapi.Parameter('id', openapi.IN_QUERY, description="Id of object to delete", type=openapi.TYPE_INTEGER)
from .models import *


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Save User Details",
    tags=["User Authentication"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_type':openapi.Schema(type=openapi.TYPE_INTEGER,description="1 for Patient, 2 for Consultant"),
            'email':openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            'password':openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
        }
    )
))
class UserView(APIView):

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user_type = request.data.get('user_type', None)
        try:
            if email is not None and password is not None and user_type is not None:
                user = User.object.filter(email=email)
                if not user.exists():
                    if user_type == 0:
                        return send_response(result=False,message="Admins cannot be created directly")
                    User.object.create_user(email=email,user_type=user_type, password=password)
                    return send_response(result=True, message="User created successfully")
                else:
                    if UserSocialAuth(user=user[0]).user_exists():
                        return send_response(result=False, message="Please login using socials")
                    return send_response(result=False, message="User with this email already exists")
            else:
                return send_response(result=False, message="Empty Fields")
        except Exception as e:
            return send_response(result=False, message=str(e))

# AUTHENTICATION EXTENDED VIEWS

@method_decorator(name="post", decorator=swagger_auto_schema(
     operation_description="Test for login",
    tags=["User Authentication"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'client_id': openapi.Schema(type=openapi.TYPE_STRING, description="Client Id (Casa Arch)"),
            'client_secret': openapi.Schema(type=openapi.TYPE_STRING, description="Client Secret (Casa Arch)"),
            'grant_type':openapi.Schema(type=openapi.TYPE_STRING, description="Should be 'password' ",),
            'username':openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="Username (Email)"),
            'password':openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description="Password")
        }
    ),
))
class TokenViewNew(TokenView):
    pass

@method_decorator(name="post", decorator=swagger_auto_schema(
     operation_description="Test for login",
    tags=["User Authentication"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'client_id': openapi.Schema(type=openapi.TYPE_STRING, description="Client Id (Casa Arch)"),
            'client_secret': openapi.Schema(type=openapi.TYPE_STRING, description="Client Secret (Casa Arch)"),
            'grant_type':openapi.Schema(type=openapi.TYPE_STRING, description="Should be 'convert_token' ",),
            'backend':openapi.Schema(type=openapi.TYPE_STRING, description="'google-oauth2' for google"),
            'token':openapi.Schema(type=openapi.TYPE_STRING, description="token"),
        }
    ),
))
class convertTokenViewNew(ConvertTokenView):
    pass


class PatientProfile(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[OAuth2Authentication,SocialAuthentication]

    def get(self,request):
        try:
            if request.user.is_anonymous:
                return send_response(result=False, message="Authentication required")
            user = User.objects.get(pk=request.user.pk)
            if Patient.objects.filter(user=user).exists():
                patient_profile = Patient.objects.get(user=user)
                data={
                    'email': user.email,
                    'profile_pic': user.profile_pic.url,
                    'name': patient_profile.name,
                    'age': patient_profile.age,
                    'gender': patient_profile.gender,
                    'history': patient_profile.history,
                    
                }
                return JsonResponse(data)
            else:
               return send_response(result=False, message="Patient Profile does not exists")
        except Exception as e:
            return send_response(result=False, message=str(e))

    def post(self,request):
        try:
            patient = Patient(user=request.user,name=request.data.get('name'),age=request.data.get('age'),gender=request.data.get('gender'),history=request.data.get('history'))
            patient.save()
            return send_response(result=True, message="Patient Profile Created Successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))

    def patch(self,request):
        try:
            if request.user.is_anonymous:
                return send_response(result=False, message="Authentication required")
            user=User.objects.get(pk=request.user.pk)
            patient=Patient.objects.get(user=user)
            serializer=PatientProfileSerializer(patient,data=request.data,partial=True)
            print(request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return send_response(result=True, message="Patient Profile Updated Successfully")
            else:
                return send_response(result=False, message="Something went wrong")
        except Exception as e:
            return send_response(result=False, message=str(e))


class ConsultantProfile(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[OAuth2Authentication,SocialAuthentication]

    def get(self,request):
        try:
            if request.user.is_anonymous:
                return send_response(result=False, message="Authentication required")
            user = User.objects.get(pk=request.user.pk)
            if Consultant.objects.filter(user=user).exists():
                consultant_profile = Consultant.objects.get(user=user)
                data={
                    'email': user.email,
                    'profile_pic': user.profile_pic.url,
                    'name': consultant_profile.name,
                    'qualification': consultant_profile.qualification,
                    'speciality': consultant_profile.speciality,
                    'clinic': consultant_profile.clinic,
                    'contact': consultant_profile.contact,
                    'bio': consultant_profile.bio,
                    'consultant_email': consultant_profile.email,
                    
                }
                return JsonResponse(data)
            else:
               return send_response(result=False, message="Consultant Profile does not exists")
        except Exception as e:
            return send_response(result=False, message=str(e))

    def post(self,request):
        try:
            consultant = Consultant(user=request.user,name=request.data.get('name'),qualification=request.data.get('qualification'),speciality=request.data.get('speciality'),clinic=request.data.get('clinic'),contact=request.data.get('contact'),email=request.data.get('email'),bio=request.data.get('bio'))
            consultant.save()
            return send_response(result=True, message="Consultant Profile Created Successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))

    def patch(self,request):
        try:
            if request.user.is_anonymous:
                return send_response(result=False, message="Authentication required")
            user = User.objects.get(pk=request.user.pk)
            consultant = Consultant.objects.get(user=user)
            serializer=ConsultantProfileSerializer(consultant,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return send_response(result=True, message="Consultant Profile Updated Successfully")
            else:
                return send_response(result=False, message="Something went wrong")
        except Exception as e:
            return send_response(result=False, message=str(e))

class ConsultantProfileAllView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[OAuth2Authentication,SocialAuthentication]

    def get(self,request):
        try:
           consultants = Consultant.objects.all()
           serializer = ConsultantProfileSerializer(consultants,many=True)
           return send_response(result=200,data=serializer.data)
        except Exception as e:
            return send_response(result=False, message=str(e)) 

class ConsultantIDView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[OAuth2Authentication,SocialAuthentication]

    def get(self,request):
        try:
           consultant = User.objects.get(pk=request.user.pk)
           serializer = UserSerializer(consultant)
           return send_response(result=200,data=serializer.data['id'])
        except Exception as e:
            return send_response(result=False, message=str(e)) 