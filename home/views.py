from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from yourfriendd.utils import send_response
from django.utils.decorators import method_decorator
from .models import *
from .serializers import PostSerializer
from django.http import JsonResponse

@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Create Contact",
    tags=["Contact"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name':openapi.Schema(type=openapi.TYPE_STRING,),
            'email':openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            'subject':openapi.Schema(type=openapi.TYPE_STRING),
            'description':openapi.Schema(type=openapi.TYPE_STRING),
        }
    )
))
class ContactView(APIView):
    def post(self,request):
        try:
            contact = Contact(name=request.data.get('name'),email=request.data.get('email'),subject=request.data.get('subject'),description=request.data.get('description'))
            contact.save()
            return send_response(result=True, message="Your Message has been sent Successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))

@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Get Posts",
    tags=["Posts"],
    
))
class PostView(APIView):
    def get(self,request):
        try:
            posts = Post.objects.all()
            serializer = PostSerializer(posts,many=True)
            return JsonResponse(serializer.data)
        except Exception as e:
            return send_response(result=False, message=str(e))