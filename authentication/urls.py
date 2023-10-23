from .views import RegistrationView, UsernameValidationView, EmailValidationView
from django.views.decorators.csrf import csrf_exempt
from django.urls import path


urlpatterns = [
    path('register_page', RegistrationView.as_view(), name="register_page"),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email',csrf_exempt(EmailValidationView.as_view()),name='validate-email')
]