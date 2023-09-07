from django.urls import path
from . import views
from .views import PhoneNumberUpload, PhoneNumberList

urlpatterns = [
    path("", views.index, name="index"),
    path("privacy/", views.privacy, name="privacy"),
    # GET request
    path("webhook/", views.whatsapp_webhook, name="whatsapp_webhook"),
    # POST request
    # path("webhook/", views.whatsapp_message, name="whatsapp_message"),
    # path("sent-message/", views.send_whatsapp_message, name="send_whatsapp_message"),
    path("phone-numbers/", PhoneNumberList.as_view(), name="phone-number-list"),
    path(
        "sent-messages/",
        views.send_whatsapp_bulk_messages,
        name="send_whatsapp_bulk_messages",
    ),
    path(
        "sent-messages/data/",
        views.send_whatsapp_model_bulk_messages,
        name="send_whatsapp_model_bulk_messages",
    ),
    path("upload/", PhoneNumberUpload.as_view(), name="upload_phone_numbers"),
]
