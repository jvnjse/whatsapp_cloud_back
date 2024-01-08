# # # tasks.py

# # from celery import shared_task
# # from datetime import datetime, timezone
# # from api.models import ScheduledAPICall


# # @shared_task
# # def make_api_call(task_id):
# #     task = ScheduledAPICall.objects.get(id=task_id)
# #     # Your API call implementation here
# #     print(
# #         f"Making API call for task: {task.id} - {task.api_data} at {datetime.now(timezone.utc)}"
# #     )
# #     # Update the task status or do any other necessary operations


# # tasks.py
# from celery import shared_task
# from django.utils import timezone


# @shared_task
# def print_hello():
#     target_datetime = timezone.datetime(2023, 1, 1, 12, 0, 0)
#     current_datetime = timezone.now()

#     if current_datetime == target_datetime:
#         print("hello")
from celery import shared_task
from django.utils import timezone


@shared_task
def print_hello():
    print("hello")


@shared_task
def schedule_hello(target_datetime):
    current_datetime = timezone.now()

    # Check if the current datetime matches the target datetime
    if current_datetime == target_datetime:
        print_hello.apply_async(countdown=5)
