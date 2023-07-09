from django.urls import path
from . import views

urlpatterns = [
    path('appointment/',views.AppointmentView.as_view(),name="appointment"),
    path('appointment/<int:pk>',views.AppointmentEditView.as_view(),name="appointment-edit"),
    path('subscription/all/',views.SubscriptionView.as_view(),name="subscription"),
    path('subscription/buy/',views.SubscriptionBuyView.as_view(),name="subscription-buy"),
    # path('selfcare/',views.SelfCareView.as_view(),name="self-care"),
    # path('selfcare/<int:pk>',views.SelfCareEditView.as_view(),name="self-care-edit"),
]