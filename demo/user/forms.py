from unittest.util import _MAX_LENGTH
from django import forms

class CreateUserPostForm(forms.Form):
    
    email = forms.CharField(label='email',max_length=64,required=True)
    password = forms.CharField(label='password',max_length=32,required=True)
    mobile_phone = forms.CharField(label='mobile_phone',min_length=10,max_length=10,required=False)
    country = forms.CharField(required=False, max_length=50)
    town = forms.CharField(required=False, max_length=20)
    address = forms.CharField(required=False, max_length=100)

class LoginPostForm(forms.Form):
    email = forms.CharField(label='email',max_length=64,required=True)
    password = password = forms.CharField(label='password',max_length=32,required=True)