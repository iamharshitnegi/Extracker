from .views import RegistrationView
from django.urls import path


urlpatterns = [
    path('register_page', RegistrationView.as_view(), name="register_page")
]