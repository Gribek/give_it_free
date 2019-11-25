from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

from GiveItFreeApp.forms import *
from GiveItFreeApp.models import TrustedInstitution, TargetGroup
from GiveItFreeApp.serializers import *


class LandingPage(View):
    """Class view for the landing page."""

    def get(self, request):
        """Display application's landing page.

        :param request: request object
        :return: landing page view
        """
        return render(request, 'GiveItFreeApp/index.html')


class MainPageUser(LoginRequiredMixin, View):
    """Class view for the main page."""

    def get(self, request):
        """Display application's main page.

        :param request: request object
        :return: main page view
        """
        ctx = {'target_groups': TargetGroup.objects.all().order_by('name')}
        return render(request, 'GiveItFreeApp/form.html', ctx)


class LoginView(View):
    """The class view that logs in users."""

    def get(self, request):
        """Display login form.

        :param request: request object
        :return: login page view
        """
        form = LoginForm()
        return render(request, 'GiveItFreeApp/login.html', {'form': form})

    def post(self, request):
        """Log in a user.

        :param request: request object
        :return: main page view or login page view with error massage
        """
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                next_view = request.GET.get('next')
                if next_view is not None:
                    return redirect(next_view)
                if user.is_superuser:
                    return redirect('/admin')
                return redirect('main_page')
            else:
                return render(request, 'GiveItFreeApp/login.html',
                              {'form': form})
        return render(request, 'GiveItFreeApp/login.html', {'form': form})


class LogoutView(View):
    """The class view that logs out users."""

    def get(self, request):
        """Log out a user.

        :param request: request object
        :return: landing page view
        """
        if request.user.is_authenticated:
            logout(request)
            return redirect('landing_page')
        else:
            return HttpResponse('Nie jesteś zalogowany')


class RegistrationView(View):
    """The class view that registers new users."""

    def get(self, request):
        """Display registration form.

        :param request: request object
        :return: registration form view
        """
        form = RegistrationForm()
        return render(request, 'GiveItFreeApp/register.html', {'form': form})

    def post(self, request):
        """Register a new user.

        :param request: request object
        :return: login page view or registration form with error
            massage
        """
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            User.objects.create_user(email=email, password=password,
                                     first_name=name, last_name=surname)
            return redirect('login')
        return render(request, 'GiveItFreeApp/register.html', {'form': form})


class EditUserProfileView(View):
    """The class view that changes user data"""

    def get(self, request):
        """Display user data edit form.

        :param request: request object
        :return: user data edit form view
        """
        current_user = request.user
        form = EditUserProfileForm(instance=current_user)
        return render(request, 'GiveItFreeApp/edit_profile.html',
                      {'form': form})

    def post(self, request):
        """Save changes to user data.

        :param request: request object
        :return: user data edit form view
        """
        form = EditUserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')
        return render(request, 'GiveItFreeApp/edit_profile.html',
                      {'form': form})


class PasswordChangeView(LoginRequiredMixin, View):
    """The class view that changes user password"""

    def get(self, request):
        """Display a password change form.

        :param request: request object
        :return: password change form view
        """
        form = PasswordChangeForm()
        return render(request, 'GiveItFreeApp/password_change.html',
                      {'form': form})

    def post(self, request):
        """Change user password.

        :param request: request object
        :return: login page view or password change form view with
            error massage
        """
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            if not request.user.is_authenticated:
                return redirect('landing_page')
            current_user = request.user
            current_user.set_password(new_password)
            current_user.save()
            return redirect('login')
        return render(request, 'GiveItFreeApp/password_change.html',
                      {'form': form})


class ProfileView(View):
    """The class view that shows all user gifts."""

    def get(self, request):
        """Display information about all user gifts.

        :param request: request object
        :return: view of all gifts prepared by a user
        """
        current_user = request.user
        gifts = Gift.objects.filter(giver=current_user).order_by(
            'creation_date', '-is_transferred', 'transfer_date')
        return render(request, 'GiveItFreeApp/profile.html', {'gifts': gifts})


class ConfirmTransferView(View):
    """The class to confirm pick up of the gift by courier."""

    def post(self, request, gift_id):
        """Confirm that gift has been handed over.

        :param request: request object
        :param gift_id: id of a gift
        :return: view of all user gifts
        """
        gift = Gift.objects.get(pk=gift_id)
        gift.is_transferred = True
        gift.transfer_date = datetime.now()
        gift.save()
        return redirect('profile')


class TrustedInstitutionsView(APIView):
    """The class that finds trusted institutions for gift form."""

    def get(self, request, format=None):
        """Search for institutions that match the criteria.

        :param request: request object
        :param format: format
        :return: serialized data about trusted institutions
        """
        trusted_institutions = TrustedInstitution.objects.all()
        if request.is_ajax():
            localization = request.GET.get('localization')
            target_groups_list = request.GET.getlist('target_groups[]')
            institution_name = request.GET.get('institution_name')
            if institution_name:
                trusted_institutions = trusted_institutions.filter(
                    name__contains=institution_name)
            if localization != '- wybierz -':
                trusted_institutions = trusted_institutions.filter(
                    localization=localization)
            if target_groups_list:
                target_groups = TargetGroup.objects.filter(
                    pk__in=target_groups_list)
                trusted_institutions = trusted_institutions.filter(
                    target_groups__in=target_groups)
        serializer = TrustedInstitutionSerializer(
            trusted_institutions, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class GiftSave(APIView):
    """The class that saves user gifts to the database."""

    def post(self, request, format=None):
        """Save information about the gift and pick up address.

        :param request: request object
        :param format: format
        :return: serialized data about the gift
        """
        if request.is_ajax:
            current_user = request.user
            address_serializer = PickUpAddressSerializer(data=request.data)
            gift_serializer = GiftSerializer(data=request.data)
            if not gift_serializer.is_valid():
                return Response(gift_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            if not address_serializer.is_valid():
                return Response(address_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            address_instance = address_serializer.save()
            gift_serializer.save(giver=current_user,
                                 pick_up_address=address_instance)
            return Response(gift_serializer.data,
                            status=status.HTTP_201_CREATED)
