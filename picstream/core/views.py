from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_backends
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from users.models import CustomUser
from codes.models import Code 
from datetime import datetime, timedelta, timezone
from django.urls import reverse

import logging
import json
import requests

API_KEY=
if API_KEY == 'WEB3_API_KEY_HERE':
    print("API key is not set")
    raise SystemExit

@login_required
def home(request):
    
    return render(request, 'core/home.html')

@login_required
def user_profile(request):
    user = request.user
    
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')

        # Update user fields
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number

        user.save()
        
        messages.success(request, 'Profil uspješno ažuriran.')
        return redirect('profile')

    images = user.images.all()

    context = {
        'user': user,
        'images': images,
    }

    return render(request, 'core/profile.html', context)

def verify_user(request):
    if request.method == 'POST':
        code_entered = request.POST.get('number')
        user_id = request.session.get('user_id')
        backend = request.session.get('backend')
        
        if user_id:
            try:
                user = CustomUser.objects.get(id=user_id)
                code_instance = user.code
                
                if code_instance.code == code_entered:
                    login(request, user, backend=backend)
                    del request.session['user_id']
                    del request.session['backend']
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid verification code')
            except Code.DoesNotExist:
                messages.error(request, 'No verification code found')
        else:
            messages.error(request, 'Session expired. Please log in again.')
            return redirect('regular_login')
        
    else:
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = CustomUser.objects.get(id=user_id)
                code_instance = user.code
                verification_code = code_instance.code
            except CustomUser.DoesNotExist:
                messages.error(request, 'User does not exist.')
                return redirect('regular_login')
        else:
            messages.error(request, 'Session expired. Please log in again.')
            return redirect('regular_login')
        
    context={
        'user_code': verification_code
    }
    
    return render(request, 'core/verify.html', context)

def login_user(request):
    return render(request, 'core/login_user.html')

def regular_login(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            backend = get_backends()[0]
            backend_path = f"{backend.__module__}.{backend.__class__.__name__}"       
            request.session['user_id'] = user.id
            request.session['backend'] = backend_path
            user.code.save()
            return redirect('verify_user')
        
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'account/login.html')
    
    return render(request, 'templates/account/login.html')

def request_message(request):
    data = json.loads(request.body)
    print(data)

    present = datetime.now(timezone.utc)
    present_plus_one_m = present + timedelta(minutes=1)
    expirationTime = str(present_plus_one_m.isoformat())
    expirationTime = str(expirationTime[:-6]) + 'Z'

    REQUEST_URL = 'https://authapi.moralis.io/challenge/request/evm'
    request_object = {
      "domain": "127.0.0.1",
      "chainId": 1,
      "address": data['address'],
      "statement": "Please confirm",
      "uri": "http://127.0.0.1:1000/",
      "expirationTime": expirationTime,
      "notBefore": "2020-01-01T00:00:00.000Z",
      "timeout": 15
    }
    x = requests.post(
        REQUEST_URL,
        json=request_object,
        headers={'X-API-KEY': API_KEY})

    return JsonResponse(json.loads(x.text))


def verify_message(request):
    data = json.loads(request.body)
    print(data)

    REQUEST_URL = 'https://authapi.moralis.io/challenge/verify/evm'
    x = requests.post(
        REQUEST_URL,
        json=data,
        headers={'X-API-KEY': API_KEY})
    print(json.loads(x.text))
    print(x.status_code)
    if x.status_code == 201:
        # user can authenticate
        eth_address=json.loads(x.text).get('address')
        print("eth address", eth_address)
        try:
            user = CustomUser.objects.get(username=eth_address)
        except CustomUser.DoesNotExist:
            user = CustomUser(username=eth_address)
            user.is_staff = False
            user.is_superuser = False
            user.save()
        if user is not None:
            if user.is_active:
                backend = get_backends()[0]
                backend_path = f"{backend.__module__}.{backend.__class__.__name__}"
                login(request, user, backend=backend_path)
                request.session['auth_info'] = data
                request.session['verified_data'] = json.loads(x.text)
                return JsonResponse({'user': user.username})
            else:
                return JsonResponse({'error': 'account disabled'})
    else:
        return JsonResponse(json.loads(x.text))
    
def moralis_auth(request):
    return render(request, 'core/moralislogin.html', {})

def moralis_profile(request):
    return render(request, 'core/moralis_profile.html', {})