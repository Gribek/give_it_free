from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from GiveItFreeApp.forms import *


# Create your views here.
class LandingPage(View):
    def get(self, request):
        return render(request, "GiveItFreeApp/index.html")


class MainPageUser(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "GiveItFreeApp/form.html")


# * * * * * Users * * * * * #

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "GiveItFreeApp/login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                next_view = request.GET.get("next")
                if next_view is not None:
                    return redirect(next_view)
                if user.is_superuser:
                    return redirect("/admin")
                return redirect("/main_page")
            else:
                return render(request, "GiveItFreeApp/login.html", {'form': form})
        return render(request, "GiveItFreeApp/login.html", {'form': form})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect("/")
        else:
            return HttpResponse("Nie jesteś zalogowany")


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "GiveItFreeApp/register.html", {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            User.objects.create_user(email=email, password=password, first_name=name, last_name=surname)
            return redirect('/login')
        return render(request, "GiveItFreeApp/register.html", {'form': form})


class EditUserProfileView(View):
    def get(self, request):
        current_user = request.user
        form = EditUserProfileForm(instance=current_user)
        return render(request, "GiveItFreeApp/edit_profile.html", {'form': form})

    def post(self, request):
        form = EditUserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("/profile")
        return render(request, "GiveItFreeApp/edit_profile.html", {'form': form})


class PasswordChangeView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm()
        return render(request, "GiveItFreeApp/password_change.html", {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get("new_password")
            if not request.user.is_authenticated:
                return redirect("/")
            current_user = request.user
            current_user.set_password(new_password)
            current_user.save()
            return redirect("/login")
        return render(request, "GiveItFreeApp/password_change.html", {'form': form})
