
from django.urls import path
from authentification.views import LoginView, HomeView, LogoutView, RegisterView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
]