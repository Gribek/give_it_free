from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from GiveItFreeApp.forms import *


# Create your views here.
class LandingPage(View):
    def get(self, request):
        return render(request, "GiveItFreeApp/index.html")


# * * * * * Users * * * * * #

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "GiveItFreeApp/login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("user")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next = request.GET.get("next")
                if next is not None:
                    return redirect(next)
                return redirect("/")
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
