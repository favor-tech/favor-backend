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
from core.views.auth import SignupView, CustomTokenObtainPairView , RefreshTokenView , LogoutView , ChangePasswordView , DeleteAccountView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), 
    path("auth/sso-login/", SSOLoginView.as_view(), name="social-login"),
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="custom-login"),
    path("auth/token/refresh/", RefreshTokenView.as_view(), name="custom-token-refresh"),
    path("auth/logout/", LogoutView.as_view(), name="custom-logout"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="custom-change-password"),
    path("auth/delete-account/", DeleteAccountView.as_view(), name="custom-delete-account"),
    path('gallerylocation-autocomplete/', GalleryLocationAutocomplete.as_view(), name='gallerylocation-autocomplete'),


]
