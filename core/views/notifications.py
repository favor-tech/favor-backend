from .base_views import GenericAPIView, Response, IsAuthenticated
from core.utils.mixins import ApiResponseMixin
from rest_framework.permissions import IsAdminUser
from core.models.device_token import DeviceToken
from core.models.notification import Notification
from core.services.firebase_service import send_push_to_user
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class RegisterDeviceTokenView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get("device_token")
        platform = request.data.get("platform", "android")

        if not token:
            return self.api_response(
                success=False,
                message="Device token is required",
                status_code=400
            )

        DeviceToken.objects.update_or_create(
            user=request.user,
            device_token=token,
            defaults={"platform": platform}
        )
        return self.api_response(success=True, message="Token registered successfully")

class SendNotificationToUserView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsAdminUser]

    def post(self, request):
        user_id = request.data.get("user_id")
        title = request.data.get("title")
        message = request.data.get("message")
        redirect_url = request.data.get("redirect_url")

        if not user_id or not title or not message:
            return self.api_response(success=False, message="Missing fields", status_code=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return self.api_response(success=False, message="User not found", status_code=404)

        send_push_to_user(user, title, message, redirect_url)

        return self.api_response(success=True, message="Notification sent to user.")

class SendNotificationToGeneralView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsAdminUser]

    def post(self, request):
        title = request.data.get("title")
        message = request.data.get("message")
        redirect_url = request.data.get("redirect_url")

        if not title or not message:
            return self.api_response(success=False, message="Title and message required", status_code=400)

        users = User.objects.all()
        for user in users:
            send_push_to_user(user, title, message, redirect_url)

        return self.api_response(success=True, message="Notification sent to all users")


class ListUserNotificationsView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-sent_at')[:10]
        data = [
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "is_read": n.is_read,
                "redirect_url": n.redirect_url,
                "sent_at": n.sent_at,
            } for n in notifications
        ]
        return self.api_response(success=True, message="Notification list", data=data)


class MarkNotificationReadView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save()
            return self.api_response(success=True, message="Notification marked as read")
        except Notification.DoesNotExist:
            return self.api_response(success=False, message="Notification not found", status_code=404)


class MarkAllNotificationsReadView(GenericAPIView, ApiResponseMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        return self.api_response(success=True, message="All notifications marked as read")
