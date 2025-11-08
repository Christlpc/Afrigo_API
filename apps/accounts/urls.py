from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, get_profile

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('profile/', get_profile, name='profile'),
]

