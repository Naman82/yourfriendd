from django.urls import path
from . import views

urlpatterns = [
    path('contact/',views.ContactView.as_view(),name="contact"),
    path('posts/all',views.PostView.as_view(),name="posts"),
]