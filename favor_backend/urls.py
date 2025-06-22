"""
URL configuration for favor_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from core.views.auth import SSOLoginView
from core.views.location_filter import GalleryLocationAutocomplete
from core.views.auth import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gallerylocation-autocomplete/', GalleryLocationAutocomplete.as_view(), name='gallerylocation-autocomplete'),
    path('', include('core.urls')), 
    
    #AUTH URLS
    path("auth/email-check/", EmailCheckView.as_view(), name="email-check"),
    path("auth/sso-login/", SSOLoginView.as_view(), name="social-login"),
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="custom-login"),
    path("auth/token/refresh/", RefreshTokenView.as_view(), name="custom-token-refresh"),
    path("auth/logout/", LogoutView.as_view(), name="custom-logout"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="custom-change-password"),
    path("auth/delete-account/", DeleteAccountView.as_view(), name="custom-delete-account"),
    path('auth/password-reset/', PasswordResetRequestView.as_view()),
    path('auth/password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view()),
    path('reset-password-form/<uidb64>/<token>/', reset_password_form, name='reset-password-form')
    #path('auth/password-reset/complete/', PasswordResetCompleteView.as_view()), #This will be required if password reset operation is managed from only Mobile UI instead of web-url link.

]
