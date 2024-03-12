# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.utils import timezone
# from .models import CustomUser, Notification


# @receiver(post_save, sender=CustomUser)
# def generate_notification_on_register_date(sender, instance, **kwargs):
#     if instance.register_date:
#         trial_period_end = instance.register_date + timezone.timedelta(days=14)
#         print("Notification")
#         if trial_period_end >= timezone.now():
#             message = (
#                 f"Your 14-day trial for user {instance.username} will expire soon."
#             )
#             Notification.objects.create(user=instance, message=message)
