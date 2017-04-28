from django import forms
from django.contrib.auth.models import User

# Allows The Password Box To Have Hidden Characters
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# Allows The Password Box To Have Hidden Characters & Username To Be A Charfield
class LoginUserForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

# Allows The Search Query Box To Be A Charfield
class TaskSearchingForm(forms.Form):
    q = forms.CharField(required=False)