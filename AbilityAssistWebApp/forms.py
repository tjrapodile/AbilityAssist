from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import validate_email
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
    username = forms.CharField(max_length= 50)
    password = forms.CharField(widget=forms.PasswordInput)

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and email != self.instance.email:
            if get_user_model().objects.filter(email=email).exists():
                raise forms.ValidationError('This email is already in use.')
        return email

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and last_name != self.instance.last_name:
            if get_user_model().objects.exclude(pk=self.instance.pk).filter(last_name=last_name).exists():
                raise forms.ValidationError('This last name is already in use.')
        return last_name

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data["last_name"]:
            user.last_name = self.cleaned_data["last_name"]
        if self.cleaned_data["email"]:
            user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


