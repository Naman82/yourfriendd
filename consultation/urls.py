from django.urls import path
from . import views

urlpatterns = [
    path('appointment/',views.AppointmentView.as_view(),name="appointment"),
    path('appointment/<int:pk>',views.AppointmentEditView.as_view(),name="appointment-edit"),
    path('subscription/',views.SubscriptionView.as_view(),name="subscription"),
    # path('selfcare/',views.SelfCareView.as_view(),name="self-care"),
    # path('selfcare/<int:pk>',views.SelfCareEditView.as_view(),name="self-care-edit"),
]