from firebase_admin import messaging
from core.models.device_token import DeviceToken
from core.models.notification import Notification
from core.models.general_notification import GeneralNotification
from core.utils.firebase_config import initialize_firebase
from django.utils import timezone

def get_all_device_tokens(user):
    return list(
        DeviceToken.objects.filter(user=user).values_list("device_token", flat=True)
    )

def send_push_to_user(user, title, message, redirect_url=None):
    initialize_firebase()

    tokens = get_all_device_tokens(user)
    if not tokens:
        return

    for token in tokens:
        msg = messaging.Message(
            token=token,
            notification=messaging.Notification(
                title=title,
                body=message
            ),
            data={"redirect_url": redirect_url or ""}
        )
        messaging.send(msg)

    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        redirect_url=redirect_url,
        is_read=False,
        sent_at=timezone.now()
    )

def send_general_notification(title, message, redirect_url=None):
    initialize_firebase()

    device_tokens = DeviceToken.objects.values_list("device_token", flat=True)

    for token in device_tokens:
        msg = messaging.Message(
            token=token,
            notification=messaging.Notification(
                title=title,
                body=message,
            ),
            data={"redirect_url": redirect_url or ""}
        )
        messaging.send(msg)

    GeneralNotification.objects.create(
        title=title,
        message=message
    )
