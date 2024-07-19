from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .serializers import *
from .models import *
from django.contrib.auth.views import LogoutView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
import requests

# Create your views here.

class DestinationCreateView(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [AllowAny]
    
class DestinationDetails(generics.RetrieveAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    
class DestinationUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    
class DestinationDetailsDelete(generics.DestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

def Reg_user(request):
    
    if request.method=='POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('password1')
        
        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.info(request, 'This username already exists')
                return redirect(request, 'registration/login.html')
            # elif User.objects.filter(email= email).exists():
            #     messages.info(request, 'This mail id already exists')
            #     return redirect(request, 'registration/login.html')
            
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
            return redirect('profile')
        
        else:
            messages.info(request, 'This password not matching')
            return redirect(request, 'registration/login.html')
        
    return redirect(request, 'registration/login.html')
    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            # login(request, user)
            auth_login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.instance.user = request.user
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=profile)
        
    destinations = Destination.objects.all()

    return render(request, 'profiles/profile.html', {'profile_form': profile_form, 'destinations': destinations})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

def create_destination(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                api_url='http://127.0.0.1:8000/create/'
                data=form.cleaned_data
                print(data)
                
                response = requests.post(api_url, data=data, files={'image':request.FILES['image']})
                print(response.status_code)
                if response.status_code == 404:
                    messages.success(request, 'Destination Added')
                    return redirect('profile')
                else:
                    messages.error(request, f'Error{response.status_code}')
            except requests.RequestException as e:
                messages.error(request, f'Error during API{str(e)}')
        else:
            messages.error(request, 'Form is not valid')
            
    else:
        form=DestinationForm()
        
    return render(request, 'profiles/create_destination.html', {'form':form})

def destination_fetch(request, id):
    api_url=f'http://127.0.0.1:8000/detail/{id}'
    response = requests.post(api_url)
    print(response.status_code)
    print(response)
    print(response.json())
    if response.status_code == 200:
        data =  response.json()
        return render(request, 'profiles/update_destination.html',{'destination':data})
    else:       
        return HttpResponseNotFound("Destination not found")

def destination_delete(request, id):
    api_url=f'http://127.0.0.1:8000/delete/{id}'
    response = requests.post(api_url)
    print(response.status_code)
    if response.status_code == 200:
        print(f'Destion of {id} has been deleted')
    else:
        print(f'Failed to delete the destination {response.status_code}')
        
    return redirect('profile')

def destination_update(request, id):
    api_url = f'http://127.0.0.1:8000/update/{id}'
    
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                data = form.cleaned_data
                response = requests.get(api_url, data=data, files={'image': request.FILES['image']})
                print(response.status_code)
                if response.status_code == 200:
                    messages.success(request, 'Destination updated successfully')
                else:
                    messages.error(request, f'Failed to update destination. Status code: {response.status_code}')
            except requests.RequestException as e:
                messages.error(request, f'Error during API request: {str(e)}')
        else:
            messages.error(request, 'Form is not valid')
    else:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            form = DestinationForm(initial=data)
        else:
            messages.error(request, f'Failed to fetch destination details. Status code: {response.status_code}')
            return redirect('profile')  
    
    return render(request, 'profiles/update_destination.html', {'form': form, 'id': id})

# def destination_fetch(request, id):
#     destination = get_object_or_404(Destination, id=id)
#     if request.method == 'POST':
#         form = DestinationForm(request.POST, request.FILES, instance=destination)
#         if form.is_valid():
#             form.save()
#             return redirect('profile') 
#     else:
#         form = DestinationForm(instance=destination)

#     return render(request, 'profiles/update_destination.html', {'form': form})