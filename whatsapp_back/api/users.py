from .models import CustomUser
from django.utils import timezone


def get_users_with_trial_ending_soon(end_date, trial_period):
    trial_start_threshold = end_date - trial_period
    users = CustomUser.objects.filter(register_date__gte=trial_start_threshold)
    return users
