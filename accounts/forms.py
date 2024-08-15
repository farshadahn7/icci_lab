from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
import re


def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return True

    else:
        return False


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'status', 'position', 'student_level', 'professor_verification', 'user_image', 'linkedin_url',
            'telegram_url',
            'user_role', 'bio')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'position', 'user_image', 'linkedin_url',
                  'telegram_url', 'bio']


class LoginForm(forms.Form):
    login = forms.CharField(max_length=128)
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def clean_login(self):
        login_value = self.cleaned_data['login']
        if '@' in login_value:
            if check(login_value):
                temp = CustomUser.objects.filter(email__iexact=login_value)
                if temp.exists():
                    return temp[0].username
                else:
                    return 'username/email or password is incorrect.'
            else:
                return 'Invalid email input'
        elif CustomUser.objects.filter(username__iexact=login_value).exists():
            return login_value
        else:
            return 'username or password is incorrect.'


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
