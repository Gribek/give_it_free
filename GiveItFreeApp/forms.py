from django import forms
from django.contrib.auth import authenticate
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from GiveItFreeApp.models import User


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('Ten adres email jest już zajęty')


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))

    def clean(self):
        super().clean()
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise ValidationError('Podane dane są niepoprawne')
        return self.cleaned_data


class RegistrationForm(forms.Form):
    email = forms.EmailField(
        validators=[validate_email], widget=forms.EmailInput(
            attrs={'placeholder': 'Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    surname = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('repeat_password')
        if password1 != password2:
            self.add_error('repeat_password',
                           'Wpisane hasła muszą byc takie same')
        return cleaned_data


class EditUserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
        }

    def clean_email(self):
        current_email = self.initial.get('email')
        email = self.cleaned_data.get('email')
        if email != current_email:
            validate_email(email)
        return email


class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Nowe hasło'}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Powtórz nowe hasło'}))

    def clean(self):
        cleaned_data = super().clean()
        field1 = cleaned_data.get('new_password')
        field2 = cleaned_data.get('repeat_password')
        if field1 != field2:
            raise ValidationError('Wpisane hasła muszą być takie same')
        return cleaned_data
