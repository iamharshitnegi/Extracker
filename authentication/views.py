from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email 
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib import auth

# Create your views here.

class EmailValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        email= data['email']

        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'},status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Sorry this email is in use.'},status=409)
        return JsonResponse({'email_valid':True})

class UsernameValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        username= data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric characters'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Sorry this username is already taken.'},status=409)
        return JsonResponse({'username_valid':True})

    
class RegistrationView(View):
    def get(self,request):
        return render(request, 'authentication/register_page.html')
    def post(self,request):
        #GET USER DATA
        #VALIDATE
        #CREATE A USER ACCOUNT

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context={
            'fieldValues':request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request, "Password too short")
                    return render(request, 'authentication/register_page.html',context)
                user=User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                # path to view
                # getting domain we are on
                # relative url for verification
                # encode uid
                # token

                uidb64= urlsafe_base64_encode(force_bytes(user.pk))
                domain=get_current_site(request).domain
                link=reverse('activate', kwargs={
                    'uidb64':uidb64, 'token':token_generator.make_token(user)
                })

                activate_url='http://'+domain+link
                email_subject = 'Activate your account'
                email_body="Hi "+user.username+". Please click on this link to verify your account\n" + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    "noreply@extractor.com",
                    [email],
                )

                email.send(fail_silently=False)

                messages.success(request, "Account successfully created.")
                return render(request, 'authentication/register_page.html')
        return render(request, 'authentication/register_page.html')
    
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
    
        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')
            
        elif not token_generator.check_token(user, token):
            messages.warning(request,'User already activated')
            return redirect('login')
            
        elif user.is_active:
            return redirect('login')

        else:
            messages.error(request, 'Activation link is invalid!')
            return redirect('login')
        

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username=request.POST['username']
        password=request.POST['password']

        if username and password:
            user= auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request, "Welcome, "+user.username+", you are now logged in.")
                    return redirect('personal_expenses')
            
                # May have to remove the next two lines of code
                messages.error(request, 'Account is not active, please check your email')
                return render(request, 'authentication/login.html')
            
            messages.error(request, 'Invalid credentials')
            return render(request, 'authentication/login.html')
        
        messages.error(request, 'Please fill all fields')
        return render(request, 'authentication/login.html')
    

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('login')


