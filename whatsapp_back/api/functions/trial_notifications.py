from datetime import datetime, timedelta
from api.models import Notification
from django.utils import timezone

# create notification when logging in


def check_trial_period(user):
    today = timezone.now().date()
    trial_period = timedelta(days=14)

    five_days_from_trial_end = today + timedelta(days=5)
    trial_start_threshold = today - trial_period

    if user.register_date <= five_days_from_trial_end:
        remaining_days = (user.register_date + trial_period - today).days
        message = f"Your trial period is ending in {remaining_days} days! Upgrade to continue using the service."
        existing_notification = Notification.objects.get(user=user)

        if existing_notification:
            existing_notification.message = message
            existing_notification.save()
        else:
            notification = Notification.objects.create(user=user, message=message)

    else:
        notification = Notification.objects.create(
            user=user,
            message="Your trial period is ending soon! Upgrade to continue using the service.",
        )
