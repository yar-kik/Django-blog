from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput,
                               label='Password')
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput,
                                label='Repeat password')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match!")
        return cd['password2']


class UserEditForm(forms.ModelForm):
    """Дозволяє користувачам змінювати ім'я, прізвише та пошту"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    """Дозволяє модифікувати додаткові відомості (дата народження, аватар)"""
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
