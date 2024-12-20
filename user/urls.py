from django.urls import path
from user.views import RegisterAPIView, LoginAPIView

app_name = 'user'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
