
from django.urls import path
from .views import *
urlpatterns = [
      path('home/',HomeView.as_view(), name ='home'),
	path('logout/', LogoutView.as_view(), name ='logout'),
      path('register/',RegisterView.as_view()),
]