"""give_it_free URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from GiveItFreeApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', LandingPage.as_view(), name='landing_page'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^main_page$', MainPageUser.as_view(), name='main_page'),
    url(r'^registration$', RegistrationView.as_view(), name='registration'),
    url(r'^edit_profile$', EditUserProfileView.as_view(),
        name='edit_profile'),
    url(r'^edit_password$', PasswordChangeView.as_view(),
        name='edit-password'),
    url(r'^trusted_institutions_list$', TrustedInstitutionsView.as_view(),
        name='trusted_institutions'),
    url(r'^gift_form_submit$', GiftSave.as_view(), name='gift_form_submit'),
    url(r'^profile$', ProfileView.as_view(), name='profile'),
    url(r'^confirm_transfer/(?P<id>\d+)$', ConfirmTransferView.as_view(),
        name='confirm_transfer'),
]
