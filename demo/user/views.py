from re import template
from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from .forms import CreateUserPostForm
from .serializer import CreateUserPayloadSerializer
from .models import User, UserProfile

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
        

        