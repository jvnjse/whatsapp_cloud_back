from celery import shared_task
from .models import ScheduledAPICall
import requests


@shared_task
def make_api_call(task_id):
    task = ScheduledAPICall.objects.get(pk=task_id)
    api_data = task.api_data

    # Replace 'API_ENDPOINT' with your actual API endpoint
    print("make_apicall")
    api_endpoint = "https://example.com/api"

    response = requests.post(api_endpoint, json=api_data)
    # Process the response or handle errors as needed
    print(response.status_code, response.json())
