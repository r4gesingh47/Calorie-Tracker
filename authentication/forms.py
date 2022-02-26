from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Profile


def validate_email(value):
    u = User.objects.filter(email=value)
    if u.exists():
        raise ValidationError('Email already exists')


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")
        labels = {
            'username': ('Username'),
            'password': ('Password'),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password'
        }

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'weight', 'height', 'bmi', 'non_veg')
