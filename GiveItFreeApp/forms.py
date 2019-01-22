from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    user = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))  # TODO zmiana logowania na email zamiast usera
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))

    def clean(self):
        username = self.cleaned_data.get('user')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Podane dane są niepoprawne")
        return self.cleaned_data
