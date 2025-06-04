
import os
import base64
import json
import requests
from jose import jwt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import User
from rest_framework_simplejwt.tokens import RefreshToken 
from jose.exceptions import JWTError
from rest_framework.authentication import BasicAuthentication
from jwt import PyJWKClient
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.utils.mixins import ApiResponseMixin
from rest_framework import serializers
from .base_views import IsAuthenticated , BasePermission


GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"
APPLE_JWKS_URL = "https://appleid.apple.com/auth/keys"

google_audience = os.getenv('GOOGLE_AUDIENCE')
apple_audience = os.getenv('APPLE_AUDIENCE')

class SSOLoginView(APIView):
    def decode_header_manually(self, id_token):
        try:
            header_b64 = id_token.split('.')[0]
            padded = header_b64 + '=' * (-len(header_b64) % 4)
            decoded = base64.urlsafe_b64decode(padded.encode())
            return json.loads(decoded)
        except Exception as e:
            print("Header decode exception:", e)
            return None


    def post(self, request):
        try:
            provider = request.data.get("provider")
            id_token = request.data.get("idToken")
            if not provider or not id_token:
                return Response({"error": "provider and idToken required"}, status=400)

            try:
                if provider == "google":
                    user_info = self.verify_firebase_google_token(id_token)
                elif provider == "apple":
                    user_info = self.verify_apple_token(id_token)
                else:
                    return Response({"error": "Invalid provider"}, status=400)
            except Exception as e:
                return Response({"error": str(e)}, status=401)

            email = user_info.get("email")
            if not email:
                return Response({"error": "Email not found in token"}, status=400)

            user, created = User.objects.update_or_create(email=email,defaults={"username": email.split("@")[0]})
            if created:
                user.username = email.split("@")[0]
                user.set_unusable_password()
                user.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "email": user.email,
                    "username": user.username
                }
            })
        except Exception as e:
            return Response({"error post": str(e)}, status=400)

    def verify_firebase_google_token(self,id_token):
        try:
            project_id = "favor-18123"
            jwks_url = "https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com"
            jwks = requests.get(jwks_url).json()
            header = self.decode_header_manually(id_token)
            key = next((k for k in jwks["keys"] if k["kid"] == header["kid"]), None)

            if not key:
                raise Exception("Firebase public key not found")

            return jwt.decode(
                id_token,
                key,
                algorithms=["RS256"],
                audience=project_id,
                issuer=f"https://securetoken.google.com/{project_id}",
            )
        except Exception as e:
            print("Firebase Google Token Exception:    " + str(e))
            return None

    def verify_apple_token(self, id_token):
        try:
            jwks = requests.get(APPLE_JWKS_URL).json()
            #unverified_header = jwt.get_unverified_header(token)
            unverified_header = self.decode_header_manually(id_token)
            key = next((k for k in jwks["keys"] if k["kid"] == unverified_header["kid"]), None)

            if not key:
                raise Exception("Apple public key not found")

            payload = jwt.decode(
                id_token,
                key,
                algorithms=["RS256"],
                audience=apple_audience,
                issuer="https://appleid.apple.com",
                options={"verify_at_hash": False}
            )
            return payload
        except Exception as e:
            print("Apple Token Login Exception:    " + str(e))
            return None





class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username_or_email = attrs.get("username")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=username_or_email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                raise serializers.ValidationError("User not found")

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")

        if not user.is_active:
            raise serializers.ValidationError("User is inactive")

        attrs["username"] = user.username
        return super().validate(attrs)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class RefreshTokenView(APIView):

    def post(self, request):
        refresh_token = request.data.get("refreshToken")

        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            return Response({"access": access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Invalid refresh token: {str(e)}"}, status=status.HTTP_401_UNAUTHORIZED)




class SignupView(APIView,ApiResponseMixin):

    def post(self, request):
        import uuid
        email = request.data.get("email")
        password = request.data.get("password")
        name = request.data.get("name")
        surname = request.data.get("surname")
        birthdate = request.data.get("birthdate")
        if not email or not name or not surname or not birthdate or not password:
            return Response({"error": "All fields are required (email, name, surname, birthdate, password)."}, status=400)

        if User.objects.filter(email=email).exists():
            return self.api_response(success=False, message="Email already exists",data=email, status_code=409)


        try:
            username = f"user_{uuid.uuid4().hex[:8]}"
            user = User.objects.create_user(
                email=email,
                username=username,
                name=name,
                surname=surname,
                birthdate=birthdate,
                password=password,
            )
        except Exception as e:
            return self.api_response(success=False, message=str(e),data=email, status_code=400)
        else:
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)

            return self.api_response(success=True, message="User created successfully.",data={
                    "email": user.email,
                    "username": user.username,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }, status_code=201)


class LogoutView(APIView,ApiResponseMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        email = user.email
        try:
            refresh_token = request.data.get("refreshToken")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return self.api_response(success=True, message="Logout successful.",data=email, status_code=200)
        except Exception as e:
            return self.api_response(success=False, message=str(e),data=email, status_code=400)


class ChangePasswordView(APIView,ApiResponseMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not user.check_password(current_password):
            return self.api_response(success=False, message="Current password is incorrect.",data=user.email, status_code=400)


        user.set_password(new_password)
        user.save()
        return self.api_response(success=True, message="Password changed successfully.",data=user.email, status_code=200)


class DeleteAccountView(APIView,ApiResponseMixin):
    permission_classes = [IsAuthenticated]


    def delete(self, request):
        user = request.user
        email = user.email
        try:
            user.delete()
        except Exception as e:
            return self.api_response(success=False, message=str(e),data=email, status_code=400)
        else:
            return self.api_response(success=True, message="Account deleted successfully.",data=email, status_code=200)


class IsGuestTokenOrAuthenticated(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get("X-Guest-Auth", "")
        guest_token = getattr(settings, "GUEST_TOKEN", "")
        if auth_header == guest_token:
            return True
        return request.user and request.user.is_authenticated