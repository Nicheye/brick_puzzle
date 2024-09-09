from main.views import InvitationView, PaymentView, StatsView
from django.urls import path

urlpatterns = [
    path('invite/', InvitationView.as_view(), name="invite"),
    path('payment/', PaymentView.as_view(), name="invite"),
    path('stats/', StatsView.as_view(), name="invite"),
]

