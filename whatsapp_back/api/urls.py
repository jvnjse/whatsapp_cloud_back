from django.urls import path
from . import views
from .views import (
    PhoneNumberUpload,
    PhoneNumberList,
    UserRegistrationView,
    UserLoginView,
)

urlpatterns = [
    path("webhook/", views.whatsapp_webhook, name="whatsapp_webhook"),
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
    path("get_templates/", views.get_templates_message, name="get_templates_message"),
    path("get_templates/lists", views.get_templates_list, name="get_templates_list"),
    path(
        "post_template/text",
        views.create_text_template,
        name="create_text_template",
    ),
    path(
        "post_template/site",
        views.create_text_template_button_site,
        name="create_text_template_button_site",
    ),
    path(
        "post_template/call",
        views.create_text_template_button_call,
        name="create_text_template_button_call",
    ),
    path(
        "upload/sent",
        views.excel_sent_message,
        name="excel_sent_message",
    ),
    path(
        "upload/data",
        views.excel_upload_message,
        name="excel_upload_message",
    ),
    path(
        "upload/image",
        views.upload_image,
        name="upload_image",
    ),
    path("upload/", PhoneNumberUpload.as_view(), name="upload_phone_numbers"),
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("", views.index, name="index"),
    path("privacy/", views.privacy, name="privacy"),
]
