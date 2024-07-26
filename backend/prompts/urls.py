
from django.urls import path
from prompts.views import MainView

urlpatterns = [
    path('', MainView.as_view()),
]