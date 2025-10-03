from django import forms
from .models import User

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        label='Confirm Password'
    )
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'username', 
            'email',
            'password'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'password': forms.PasswordInput(attrs={'class': 'form-input'}),
        }
