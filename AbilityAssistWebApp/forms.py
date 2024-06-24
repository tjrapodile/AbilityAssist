import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import requests
from django.core.validators import validate_email, RegexValidator
from django.core.exceptions import ValidationError


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    username = forms.CharField(max_length=10,validators=[RegexValidator(regex=r'^\d{10}$', message="Enter a valid 10-digit phone number.")], help_text='Required. Enter your phone number.')
    first_name = forms.CharField(max_length=30, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, help_text='Required. Enter your last name.')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Password confirmation')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        debug_messages = []
        if User.objects.filter(username=username).exists():
            debug_messages.append("Phone number already in use.")
            raise forms.ValidationError("This phone number is already in use.")
        if not re.match(r'^(06|07|08)\d{8}$', username):
            debug_messages.append("Invalid phone number pattern.")
            raise forms.ValidationError("Enter a valid South African 10-digit phone number.")

        api_key = '3cef86b5210bb14cbcca6382cebc6532'
        api_url = f'http://apilayer.net/api/validate?access_key={api_key}&number={username}&country_code=ZA&format=1'
        try:
            response = requests.get(api_url)
            debug_messages.append(f"API response status code: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            debug_messages.append(f"API response data: {data}")

            if not data.get('valid', False) or data.get('line_type') != 'mobile':
                debug_messages.append("Phone number not valid.")
                raise forms.ValidationError("The phone number is not valid or not registered as a mobile number.")
        except requests.RequestException:
            debug_messages.append(f"RequestException occurred")
            raise forms.ValidationError("Failed to validate phone number. Please try again later.")
        print("\n".join(debug_messages))  # Print debug messages to the console
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

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("This phone number does not exist.")
        return username


class EditUserForm(forms.ModelForm):

    username = forms.CharField(max_length=10, required=False, validators=[
        RegexValidator(regex=r'^\d{10}$', message="Enter a valid 10-digit phone number.")],
        help_text='Optional. Enter a new phone number if you wish to change it.')

    class Meta:
        model = get_user_model()
        fields = ['email', 'last_name', 'username']

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.username

    def clean_username(self):
        username = self.cleaned_data.get('username')
        debug_messages = []
        if username and username != self.instance.username:
            if User.objects.filter(username=username).exists():
                debug_messages.append("Phone number already in use.")
                raise forms.ValidationError("This phone number is already in use.")
            if not re.match(r'^(06|07|08)\d{8}$', username):
                debug_messages.append("Invalid phone number pattern.")
                raise forms.ValidationError("Enter a valid South African 10-digit phone number.")

            api_key = '3cef86b5210bb14cbcca6382cebc6532'
            api_url = f'http://apilayer.net/api/validate?access_key={api_key}&number={username}&country_code=ZA&format=1'
            try:
                response = requests.get(api_url)
                debug_messages.append(f"API response status code: {response.status_code}")
                response.raise_for_status()
                data = response.json()
                debug_messages.append(f"API response data: {data}")

                if not data.get('valid', False) or data.get('line_type') != 'mobile':
                    debug_messages.append("Phone number not valid.")
                    raise forms.ValidationError("The phone number is not valid or not registered as a mobile number.")
            except requests.RequestException:
                debug_messages.append(f"RequestException occurred")
                raise forms.ValidationError("Failed to validate phone number. Please try again later.")
            print("\n".join(debug_messages))  # Print debug messages to the console
        else:
            return self.instance.username
        return username


    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and any(char.isdigit() or not char.isalnum() for char in last_name):
            raise forms.ValidationError('Last name should not contain numbers or special characters.')
        return last_name

    def save(self, commit=True, request=None, user=None):
        user = user = self.instance
        print("Request:", request)
        print("User ID:", user.id)
        print("User username:", user.username)
        cleaned_email = self.cleaned_data.get('email')
        cleaned_last_name = self.cleaned_data.get('last_name')
        cleaned_username = self.cleaned_data.get('username')
        print("Cleaned username:", cleaned_username)  # Debugging message
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
            user.last_name = cleaned_last_name
            print("Updated last_name:", user.last_name)  # Add this line
        else:
            print("Existing last_name:", user.last_name)
            print("Last name not updated, retaining existing value.")  # Debugging message

        if cleaned_username and cleaned_username.strip() != '':
            print("Updating username...")  # Debugging message
            print("Existing username:", user.username)  # Add this line
            print("Updated username:", user.username)  # Add this line
            user.username = cleaned_username
        else:
            print("Existing username:", user.username)
            print("Mobile Number not updated, retaining existing value.")  # Debugging message

        if commit:
            print("Saving user...")  # Debugging message
            user.save()

        print("User saved successfully.")  # Debugging message
        return user
