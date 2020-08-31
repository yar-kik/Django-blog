from django import forms
from django.contrib.auth.models import User
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import Profile
from phonenumber_field.formfields import PhoneNumberField


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput,
                               label='Password')

    class Meta:
        model = User
        fields = ('username', 'email')


class UserEditForm(forms.ModelForm):
    """Дозволяє користувачам змінювати ім'я, прізвише та пошту"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'example@gmail.com'})
        }


class ProfileEditForm(forms.ModelForm):
    """Дозволяє модифікувати додаткові відомості (дата народження, аватар)"""

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo', 'sex', 'phone')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'placeholder': 'ДД.ММ.РРРР'}),
            'phone': forms.DateInput(attrs={'placeholder': '+380(__)___-__-__'})
        }
        error_messages = {
            'phone': {
                'invalid': 'Введіть коректний номер телефону, наприклад +38(098)152-27-15',
                'unique': "Вибачте, але на цей номер вже зареєстровано інший акаунт"
            },
            'date_of_birth': {
                'invalid': 'Введіть коректну дату народження',
            }
        }
