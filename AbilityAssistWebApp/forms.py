from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone = forms.CharField(max_length=10, help_text='Required. Enter your phone number.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Invalid email address")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        # Validate phone number to ensure it contains only digits and has exactly 10 digits
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Invalid phone number. Please enter a 10-digit number.")
        return phone

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        # Add custom password validation logic here
        # For example, ensure the password has at least 8 characters and contains a mix of letters and numbers
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password1) or not any(char.isalpha() for char in password1):
            raise forms.ValidationError("Password must contain both letters and numbers")
        return password1


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
