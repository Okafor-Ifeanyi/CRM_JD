from django import forms
from leads.models import User 
# from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm



class AgentModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
        )