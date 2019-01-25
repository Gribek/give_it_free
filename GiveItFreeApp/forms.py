from django import forms
from django.contrib.auth import authenticate
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from GiveItFreeApp.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise ValidationError("Podane dane są niepoprawne")
        return self.cleaned_data


class RegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))

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


class EditUserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {'email': forms.TextInput(attrs={'placeholder': 'Email'}),
                   'first_name': forms.TextInput(attrs={'placeholder': 'Imię'}),
                   'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
                   }


class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(label="Nowe hasło", widget=forms.PasswordInput)
    repeat_password = forms.CharField(label="Powtórz nowe hasło", widget=forms.PasswordInput)

    def clean(self):
        cleaned_date = super().clean()
        field1 = cleaned_date.get('new_password')
        field2 = cleaned_date.get('repeat_password')
        if field1 != field2:
            raise ValidationError("Wpisane hasła muszą być takie same")
        return cleaned_date
