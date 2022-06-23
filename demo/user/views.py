from multiprocessing import AuthenticationError
from re import template
from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from .forms import CreateUserPostForm, LoginPostForm
from .serializer import CreateUserPayloadSerializer, UserLoginPayloadSerializer
from .models import User, UserProfile
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def create_user(request):
    create_user_template_name = 'create_user.html'
    if request.method == 'GET':
        return render(request,create_user_template_name)
    if request.method == 'POST':
        form = CreateUserPostForm(request.POST)
        if form.is_valid():
            create_user_payload={}
            create_user_profile_payload={}
            create_user_payload['username'] = form.cleaned_data['username']
            create_user_payload['email'] = form.cleaned_data['email']
            create_user_payload['password'] = form.cleaned_data['password']
            create_user_profile_payload['country'] = form.cleaned_data['country']
            create_user_profile_payload['mobile_phone'] = form.cleaned_data['mobile_phone']
            create_user_profile_payload['address'] = form.cleaned_data['address']
            serializer = CreateUserPayloadSerializer(data=create_user_payload)
            serializer.is_valid(raise_exception=True)
            user = User.objects.create(**create_user_payload)
            create_user_profile_payload['user'] = user
            UserProfile.objects.create(**create_user_profile_payload)
            if create_user_payload['password']:
                user.set_password(create_user_payload['password'])
                user.save()
            return HttpResponse(200)
        return HttpResponse(400)
        
def user_login(request):
    login_template_name = 'login.html'
    if request.method == 'GET':
        return render(request,login_template_name)
    if request.method == 'POST':
        form = LoginPostForm(request.POST)
        if form.is_valid():
            login_payload = {}
            login_payload['email'] = form.cleaned_data['email']
            login_payload['password'] = form.cleaned_data['password']
            serializer = UserLoginPayloadSerializer(data=login_payload)
            serializer.is_valid(raise_exception=True)
            login_user = authenticate(request, username=login_payload['email'], password=login_payload['password'])
            if login_user:
                login(request, login_user)
                return HttpResponse(200)
            else:
                return HttpResponse(401)
            
        
        