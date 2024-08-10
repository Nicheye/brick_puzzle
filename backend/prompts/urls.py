
from django.urls import path
from prompts.views import MainView, ShareView, CommonPicView

urlpatterns = [
    path('', MainView.as_view()),
    path('share', ShareView.as_view()),
    path('pic', CommonPicView.as_view()),
]
