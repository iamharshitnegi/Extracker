from .views import RegistrationView, UsernameValidationView, EmailValidationView, VerificationView, LoginView
from django.views.decorators.csrf import csrf_exempt
from django.urls import path


urlpatterns = [
    path('register_page', RegistrationView.as_view(), name="register_page"),
    path('login', LoginView.as_view(), name="login"),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email',csrf_exempt(EmailValidationView.as_view()),name='validate-email'),
    path('activate/<uidb64>/<token>',VerificationView.as_view(),name="activate" )
]