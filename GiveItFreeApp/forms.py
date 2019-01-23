from django import forms
from django.contrib.auth import authenticate
from GiveItFreeApp.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Podane dane są niepoprawne")
        return self.cleaned_data


class RegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('repeat_password')
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', "Ten adres email jest już zajęty")
        if password1 != password2:
            self.add_error("repeat_password", "Wpisane hasła muszą byc takie same")
        return cleaned_data
