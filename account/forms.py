from django import forms
from django.contrib.auth.models import User
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from konfetka import settings
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

    def clean_photo(self):
        max_photo_size = settings.MAX_UPLOAD_IMAGE_SIZE
        valid_extensions = settings.VALID_IMAGE_EXTENSION
        photo = self.cleaned_data['photo']
        photo_format = photo.name.split('.')[-1]
        if photo_format in valid_extensions:
            if photo.size > max_photo_size:
                raise forms.ValidationError("Розмір вашого зображення перевищує 2 Мб!")
        else:
            raise forms.ValidationError('Будь ласка, виберіть зображення у форматі jpg, jpeg або png')
        return photo

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


class FeedbackEmailForm(forms.Form):
    """Форма для відгуків, пропозицій, скарг.
    Атрибути:
    subject - тема листа;
    sender - пошта відправника;
    message - зміст повідомлення;
    """
    subject = forms.CharField(max_length=100)
    sender = forms.EmailField()
    message = forms.CharField(max_length=5000, widget=forms.Textarea)