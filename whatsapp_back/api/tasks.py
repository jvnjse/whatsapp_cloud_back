# # # # tasks.py

from celery import shared_task

# from datetime import datetime, timezone
# from api.models import ScheduledAPICall


# @shared_task
# def make_api_call(task_id):
#     task = ScheduledAPICall.objects.get(id=task_id)
#     print(
#         f"Making API call for task: {task.id} - {task.api_data} at {datetime.now(timezone.utc)}"
#     )


# # # tasks.py
# # from celery import shared_task
# # from django.utils import timezone


# # @shared_task
# # def print_hello():
# #     target_datetime = timezone.datetime(2023, 1, 1, 12, 0, 0)
# #     current_datetime = timezone.now()

# #     if current_datetime == target_datetime:
# #         print("hello")
# from celery import shared_task
# from django.utils import timezone


# @shared_task
# def print_hello():
#     print("hello")


# @shared_task
# def schedule_hello(target_datetime):
#     current_datetime = timezone.now()

#     # Check if the current datetime matches the target datetime
#     if current_datetime == target_datetime:
#         print_hello.apply_async(countdown=5)

# from datetime import timedelta

# # from django.core.mail import send_mail
# from django.utils import timezone

# from .models import Notification
# from .users import get_users_with_trial_ending_soon


# def check_trial_periods():
#     today = timezone.now()
#     trial_period = timedelta(days=14)

#     print("cscjh")
#     five_days_from_trial_end = today + timedelta(days=5)
#     users_to_notify = get_users_with_trial_ending_soon(
#         five_days_from_trial_end, trial_period
#     )

#     for user in users_to_notify:
#         notification = Notification.objects.create(
#             user=user,
#             message="Your trial period is ending soon! Upgrade to continue using the service.",
#         )
#         # Optionally send email notification (replace with your email settings)
#         # send_mail(
#         #     subject="Your Trial Period is Ending Soon",
#         #     message=notification.message,
#         #     from_email="your_email@example.com",
#         #     recipient_list=[user.email],
#         # )


# @shared_task
# def schedule_trial_check():
#     check_trial_periods()
# check_trial_periods(timezone.now(), timezone.now() + timedelta(days=5))
