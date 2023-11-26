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
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here.

class EmailValidationView(View):
    def post(self,request):
        # Validate the email provided in the request
        data=json.loads(request.body)
        email= data['email']

        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'},status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Sorry this email is in use.'},status=409)
        return JsonResponse({'email_valid':True})

class UsernameValidationView(View):
    def post(self,request):
        # Validate the username provided in the request
        data=json.loads(request.body)
        username= data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric characters'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Sorry this username is already taken.'},status=409)
        return JsonResponse({'username_valid':True})

    
class RegistrationView(View):
    def get(self,request):
        # Render the registration page
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

                # Generate activation link
                uidb64= urlsafe_base64_encode(force_bytes(user.pk))
                domain=get_current_site(request).domain
                link=reverse('activate', kwargs={
                    'uidb64':uidb64, 'token':token_generator.make_token(user)
                })

                activate_url='http://'+domain+link

                # Send activation email
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
        # Verify user account using uidb64 and token
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
    
        if user is not None and token_generator.check_token(user, token):
            # Activate the user account
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
         # Render the login page
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        # Handle user login
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
        # Log out the user
        auth.logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('login')

class RequestPasswordResetEmail(View):
    def get(self, request):
        # Render the password reset request page
        return render(request, 'authentication/reset_password.html')

    def post(self, request):
        # Handle the request for password reset email
        email = request.POST

        context:{
            'values': request.POST
        }

        if not validate_email(email):
            messages.error(request, 'Please give a valid email')
            return render(request, 'authentication/reset_passwowrd.html', context)    

        domain=get_current_site(request).domain

        user = request.objects.filter(email=email)

        uidb64= urlsafe_base64_encode(force_bytes(user.pk))

        if user.exists():
            link=reverse('reset-user-password', kwargs={
                    'uidb64':uidb64, 'token':PasswordResetTokenGenerator().make_token(user)
                })

            reset_url='http://'+domain+link
            email_subject = 'Reset your password'
            email_body="Hi "+user.username+". Please click on this link to reset your password\n" + reset_url
            email = EmailMessage(
                email_subject,
                email_body,
                "noreply@extractor.com",
                [email],
            )

            email.send(fail_silently=False)

        messages.succes(request, "we have sent you an email to reset your password")
        

        return render(request, 'authentication/reset_passwowrd.html')    
    

class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        # Render the page for completing password reset
        context = {
            'uidb64': uidb64,
            'token': token
        }

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password link is invalid, Please rquest a new one')
                return render(request, 'authenticatoin/set_new_password.html')
    
        except Exception as identifier:
           pass

        return render(request, 'authenticatoin/set_new_password.html', context)
    
    def post(self, request, uidb64, token):
        # Handle the completion of password reset
        context = {
            'uidb64': uidb64,
            'token': token
        }

        password=request.POST['password']
        password2=request.POST['password2']

        if password!=password2:
            messages.error(request, "Passwords don't match")
            return render(request, 'authenticatoin/set_new_password.html', context)

        if len(password) < 6:
            messages.error(request, 'Password too short')
            return render(request, 'authenticatoin/set_new_password.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.password = password
            user.save()

            messages.success(request, 'Password reset successfull, you can login with your new password')
            return redirect('login')
    
        except Exception as identifier:
            messages.info(request, 'Something went wrong, try again')
            return render(request, 'authenticatoin/set_new_password.html', context)

       

        # return render(request, 'authenticatoin/set_new_password.html', context)