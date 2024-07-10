from django import forms
from .models import *

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name' , 'gender', 'mobile_no', 'email']
        
class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = '__all__'