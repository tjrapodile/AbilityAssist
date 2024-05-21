import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import validate_email, RegexValidator
from django.core.exceptions import ValidationError


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    username = forms.CharField(max_length=15, help_text='Required. Create your username.')
    first_name = forms.CharField(max_length=30, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, help_text='Required. Enter your last name.')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Password confirmation')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use.")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not re.match(r'^[A-Za-z\s]+$', first_name):
            raise forms.ValidationError("Only alphabetic characters are allowed in the first name.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not re.match(r'^[A-Za-z\s]+$', last_name):
            raise forms.ValidationError("Only alphabetic characters are allowed in the last name.")
        return last_name


    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Invalid email address")
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not password1 or not password2:
            raise forms.ValidationError("Both password fields are required")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class EditUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'last_name']

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and any(char.isdigit() or not char.isalnum() for char in last_name):
            raise forms.ValidationError('Last name should not contain numbers or special characters.')
        return last_name

    def save(self, commit=True, request=None, user=None):
        user = User.objects.get_by_natural_key(user.username)
        print("Request:", request)
        print("User ID:", user.id)
        print("User username:", user.username)
        cleaned_email = self.cleaned_data.get('email')
        cleaned_last_name = self.cleaned_data.get('last_name')

        print("Cleaned email:", cleaned_email)  # Debugging message
        print("Cleaned last name:", cleaned_last_name)  # Debugging message

        if cleaned_email and cleaned_email.strip() != '':
            print("Updating email...")  # Debugging message
            print("Existing email:", user.email)  # Add this line
            user.email = cleaned_email
            print("Updated email:", user.email)  # Add this line
        else:
            print("Existing email:", user.email)
            print("Email not updated, retaining existing value.")  # Debugging message

        if cleaned_last_name and cleaned_last_name.strip() != '':
            print("Updating last name...")  # Debugging message
            print("Existing last_name:", user.last_name)  # Add this line
            print("Updated last_name:", user.last_name)  # Add this line
            user.last_name = cleaned_last_name
        else:
            print("Existing last_name:", user.last_name)
            print("Last name not updated, retaining existing value.")  # Debugging message

        if commit:
            print("Saving user...")  # Debugging message
            user.save()

        print("User saved successfully.")  # Debugging message
        return user
