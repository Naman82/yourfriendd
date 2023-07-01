from . import views 
from django.urls import path, include, re_path


urlpatterns = [
    re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('user-signup', views.UserView.as_view(), name='user-signup'),
    path('user-login', views.TokenViewNew.as_view(), name='token'),
    path('user-convert-token', views.convertTokenViewNew.as_view(), name='convert-token'),

    path('patient/profile/',views.PatientProfile.as_view(),name='patient-profile'),
    path('consultant/profile/',views.ConsultantProfile.as_view(),name='consultant-profile'),
    path('consultant/profile/all/',views.ConsultantProfileAllView.as_view(),name='consultant-profile-all'),
    path('consultant/id/',views.ConsultantIDView.as_view(),name='consultant-id'),
]