from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import User  # kendi User modelin
from rest_framework_simplejwt.tokens import RefreshToken  # JWT kullanıyorsan
import requests
from jose import jwt

GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"
APPLE_JWKS_URL = "https://appleid.apple.com/auth/keys"

class SSOLoginView(APIView):
    def post(self, request):
        provider = request.data.get("provider")
        id_token = request.data.get("idToken")

        if not provider or not id_token:
            return Response({"error": "provider and idToken required"}, status=400)

        try:
            if provider == "google":
                user_info = self.verify_google_token(id_token)
            elif provider == "apple":
                user_info = self.verify_apple_token(id_token)
            else:
                return Response({"error": "Invalid provider"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=401)

        email = user_info.get("email")
        if not email:
            return Response({"error": "Email not found in token"}, status=400)

        user, created = User.objects.get_or_create(email=email)
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

    def verify_google_token(self,id_token):
        jwks = requests.get('https://www.googleapis.com/oauth2/v3/certs').json()
        unverified_header = jwt.get_unverified_header(id_token)
        key = next((k for k in jwks["keys"] if k["kid"] == unverified_header["kid"]), None)

        if not key:
            raise Exception("Google public key not found")

        try:
            payload = jwt.decode(
                id_token,
                key,
                algorithms=['RS256'],
                audience='287284407475-3tt51oqv8v12k5sn1746mu6glvkq07sm.apps.googleusercontent.com',
                options={"verify_at_hash": False}
            )
            return payload
        except jwt.JWTError as e:
            raise Exception(f"Invalid token: {str(e)}")

    def verify_apple_token(self, token):
        jwks = requests.get(APPLE_JWKS_URL).json()
        unverified_header = jwt.get_unverified_header(token)
        key = next((k for k in jwks["keys"] if k["kid"] == unverified_header["kid"]), None)

        if not key:
            raise Exception("Apple public key not found")

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience="com.favorteknoloji.favor",
            issuer="https://appleid.apple.com",
            options={"verify_at_hash": False}
        )
        return payload
