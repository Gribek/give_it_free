from django import forms
from django.contrib.auth import authenticate
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from GiveItFreeApp.models import User


def validate_email(value):
    """Check if email is not used.

    :param value: email
    :return: None
    """
    if User.objects.filter(email=value).exists():
        raise ValidationError('Ten adres email jest już zajęty')


def validate_repeat_password(password, repeat_password):
    """Check if password and repeat_password are the same.

    :param password: password
    :param repeat_password: repeat password
    :return: None
    """
    if password != repeat_password:
        raise ValidationError('Wpisane hasła muszą byc takie same')


class LoginForm(forms.Form):
    """User login form."""

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))

    def clean(self):
        """Validate user email and password.

        :return: validated data
        """
        super().clean()
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise ValidationError('Podane dane są niepoprawne')
        return self.cleaned_data


class RegistrationForm(forms.Form):
    """User registration form."""

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

    def clean_repeat_password(self):
        """Validate repeat password.

        :return: repeat password
        """
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        validate_repeat_password(password, repeat_password)
        return repeat_password


class EditUserProfileForm(ModelForm):
    """User profile editing form."""

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
        }

    def clean_email(self):
        """Validate email.

        :return: email
        """
        current_email = self.initial.get('email')
        email = self.cleaned_data.get('email')
        if email != current_email:
            validate_email(email)
        return email


class PasswordChangeForm(forms.Form):
    """User password change form."""

    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Nowe hasło'}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Powtórz nowe hasło'}))

    def clean_repeat_password(self):
        """Validate repeat password.

        :return: repeat password
        """
        password = self.cleaned_data.get('new_password')
        repeat_password = self.cleaned_data.get('repeat_password')
        validate_repeat_password(password, repeat_password)
        return repeat_password
