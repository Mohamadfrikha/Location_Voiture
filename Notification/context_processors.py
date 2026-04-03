
from .models import Notification

def notificationUser(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by("-date_envoi")
        return {
            "notifications": notifications[:5],
            "nb_notification": notifications[:5].count()
        }
    return {
        "notifications": [],
        "nb_notification": 0
    }