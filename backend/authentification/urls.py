
from django.urls import path
from authentification.views import LoginView, LogoutView, RegisterView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
]