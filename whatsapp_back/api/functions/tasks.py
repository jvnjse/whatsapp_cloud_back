from celery import shared_task
from api.models import PhoneNumber
import logging
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import requests, json

logger = logging.getLogger(__name__)


@shared_task
def send_message_to_facebook_excel_normal(
    excel, template_name, user_id, phone_number_id, bearer_token
):
    try:
        logger.info("Excel Data: %s", excel)
        results = []
        # excel_data = pd.read_json(excel_data_json)
        for value in excel:
            raw_number = str(value).replace(" ", "")
            if raw_number and (raw_number.startswith("91")) and (len(raw_number) == 12):
                raw_number = "+" + raw_number
            elif raw_number and raw_number.startswith("0"):
                raw_number = "+91" + raw_number[1:]
            print(raw_number)

            if raw_number:
                PhoneNumber.objects.get_or_create(number=raw_number, user_id=user_id)

                data = {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": raw_number,
                    "type": "template",
                    "template": {"name": template_name, "language": {"code": "en"}},
                }

                url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
                headers = {
                    "Authorization": "Bearer " + bearer_token,
                    "Content-Type": "application/json",
                }

                try:
                    response = requests.post(url, headers=headers, json=data)
                    response_data = response.json()
                    results.append(response_data)
                except json.JSONDecodeError:
                    pass
        return "None"

        # return results
    except Exception as e:
        # logger.exception("An error occurred in send_message_to_facebook task: %s", e)
        # print("dscjbjhb")

        raise e


@shared_task
def send_message_to_facebook_excel_images(
    excel, template_name, user_id, phone_number_id, bearer_token, image_link_get
):
    try:
        logger.info("Excel Data: %s", excel)
        results = []
        # excel_data = pd.read_json(excel_data_json)
        for value in excel:
            raw_number = str(value).replace(" ", "")
            if raw_number and (raw_number.startswith("91")) and (len(raw_number) == 12):
                raw_number = "+" + raw_number
            elif raw_number and raw_number.startswith("0"):
                raw_number = "+91" + raw_number[1:]
            print(raw_number)

            if raw_number:
                PhoneNumber.objects.get_or_create(number=raw_number, user_id=user_id)

                data = {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": raw_number,
                    "type": "template",
                    "template": {
                        "name": template_name,
                        "components": [
                            {
                                "type": "header",
                                "parameters": [
                                    {
                                        "type": "image",
                                        "image": {"link": image_link_get},
                                    }
                                ],
                            }
                        ],
                        "language": {"code": "en"},
                    },
                }
                print(data)
                url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
                headers = {
                    "Authorization": "Bearer " + bearer_token,
                    "Content-Type": "application/json",
                }

                try:
                    response = requests.post(url, headers=headers, json=data)
                    response_data = response.json()
                    results.append(response_data)
                    print(results)
                except json.JSONDecodeError:
                    pass
        return "None"

        # return results
    except Exception as e:
        # logger.exception("An error occurred in send_message_to_facebook task: %s", e)
        # print("dscjbjhb")

        raise e


@shared_task
def send_email(email, password):
    my_subject = "Whatsapp Module Generated Password"
    context = {
        "password": password,
    }
    recipient_list = [email]
    html_message = render_to_string("password.html", context)
    plain_message = strip_tags(html_message)
    message = EmailMultiAlternatives(
        subject=my_subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list,
    )
    message.attach_alternative(html_message, "text/html")
    message.send()
    # return None
