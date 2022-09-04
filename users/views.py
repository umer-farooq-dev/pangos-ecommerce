from django.contrib.sites import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import uuid
from online.models import *
from django.core.mail import send_mail
# Create your views here.
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from online.models import Customer
from users.forms import CustomerRegistrationForm, CustomerProfileForm, LoginForm


def send_email(email, token):
    send_mail(
        'Verify Email',
        f'Hi Click on the link to verify your account http://127.0.0.1:8000/account-verify/{token}',
        'ibsoft0786@gmail.com',
        [email],
        fail_silently=False,
        # subject="Verify Email",
        # message=f'Hi Click on the link to verify your account http://127.0.0.1:8000/account-verify/{token}',
        # from_email=settings.EMAIL_HOST_USER,
        # recipient_list=[email],
        # fail_silently=False,
    )


def account_verify(request, token):
    pf = VerifiedEmail.objects.filter(token=token).first()
    pf.verify = True
    pf.save()
    messages.success(request, "Your account has been verified, you can login")
    return redirect('/registration/')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            uid = uuid.uuid4()
            email_v = VerifiedEmail(user=new_user, token=uid)
            email_v.save()
            send_email(new_user.email, uid)
            messages.success(request,
                             'Congratulations!! Registered Successfully, To verify your account Check your Email')
        return render(request, 'users/register.html', {'form': form})


class SignInView(View):
    def get(self, request):
        fm = LoginForm()
        return render(request, 'users/login.html', {'form': fm})

    def post(self, request):
        fm = LoginForm(request, data=request.POST)
        if fm.is_valid():
            username = fm.cleaned_data['username']
            password = fm.cleaned_data['password']

            user = authenticate(username=username, password=password)
            pro = VerifiedEmail.objects.get(user=user)
            if pro.verify:
                login(request, user)
                return redirect('/profile/')
            else:
                messages.info(request, "Your account is not verified, please check your email, and verify your account")
                return redirect('/registration')
