from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(
        max_length=15,
        required=True,
        help_text="Enter a valid phone number."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone.isdigit():
            raise forms.ValidationError(
                "Phone number should contain only digits.")
        if len(phone) < 10 or len(phone) > 15:
            raise forms.ValidationError(
                "Enter a valid phone number (10-15 digits).")
        return phone


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=15,
        required=True,
        help_text="Enter a valid phone number."
    )

    class Meta:
        model = Profile
        fields = ['image', 'phone', 'fitness_goal', 'fitness_level', 'plan']

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone.isdigit():
            raise forms.ValidationError(
                "Phone number should contain only digits.")
        if len(phone) < 10 or len(phone) > 15:
            raise forms.ValidationError(
                "Enter a valid phone number (10-15 digits).")
        return phone
        
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = Profile
        fields = [
            'image', 'phone', 'fitness_goal', 'fitness_level', 
            'height', 'weight', 'date_of_birth'
        ]
        widgets = {
            'height': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Height in cm'}),
            'weight': forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'Weight in kg'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(
        max_length=15,
        required=True,
        help_text="Enter a valid phone number."
    )
    message = forms.CharField(widget=forms.Textarea)

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone.isdigit():
            raise forms.ValidationError(
                "Phone number should contain only digits.")
        if len(phone) < 10 or len(phone) > 15:
            raise forms.ValidationError(
                "Enter a valid phone number (10-15 digits).")
        return phone
