from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

# from .views import (
#     PhoneNumberUpload,
#     PhoneNumberList,
#     UserRegistrationView,
#     UserLoginView,
#     UserListView,
#     UserDetailView,
#     validate_access_token,
# )

urlpatterns = [
    path(
        "user-hierarchy/<int:pk>/",
        UserHierarchyView.as_view(),
        name="user-hierarchy-detail",
    ),
    path(
        "user-children/<int:pk>/",
        UserChildrenListView.as_view(),
        name="user-children-list",
    ),
    path("webhook/", views.whatsapp_webhook, name="whatsapp_webhook"),
    path("phone-numbers/", PhoneNumberList.as_view(), name="phone-number-list"),
    path("users/", UserListView2.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-list-detail"),
    path(
        "sent-messages/",
        views.send_whatsapp_bulk_messages,
        name="send_whatsapp_bulk_messages",
    ),
    path(
        "sent-messages/images",
        views.send_whatsapp_bulk_messages_images,
        name="send_whatsapp_bulk_messages_images",
    ),
    path(
        "sent-messages/data/",
        views.send_whatsapp_model_bulk_messages,
        name="send_whatsapp_model_bulk_messages",
    ),
    path(
        "sent-messages/data/images",
        views.send_whatsapp_model_bulk_messages_images,
        name="send_whatsapp_model_bulk_messages_images",
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
        "post_template/text/personalised",
        views.create_text_template_personalised,
        name="create_text_template_personalised",
    ),
    path(
        "post_template/site/personalised",
        views.create_text_template_button_site_personalised,
        name="create_text_template_button_site_personalised",
    ),
    path(
        "post_template/call/personalised",
        views.create_text_template_button_call_personalised,
        name="create_text_template_button_call_personalised",
    ),
    path(
        "post_template/image",
        views.create_image_template,
        name="create_image_template",
    ),
    path(
        "post_template/image/personalised",
        views.create_image_template_personalised,
        name="create_image_template_personalised",
    ),
    path(
        "post_template/image/url",
        views.create_image_template_url,
        name="create_image_template_url",
    ),
    path(
        "post_template/image/call",
        views.create_image_template_call,
        name="create_image_template_call",
    ),
    path(
        "upload/sent",
        views.excel_sent_message,
        name="excel_sent_message",
    ),
    path(
        "upload/sent/personalised",
        views.excel_personalised_sent_message,
        name="excel_personalised_sent_message",
    ),
    path(
        "upload/sent/images",
        views.excel_sent_message_images,
        name="excel_sent_message_images",
    ),
    path(
        "upload/sent/images/personalised",
        views.excel_sent_message_images_personalised,
        name="excel_sent_message_images_personalised",
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
    path(
        "delete/template",
        views.delete_template,
        name="delete_template",
    ),
    path(
        "upload/credentials",
        views.upload_credentials,
        name="upload_credentials",
    ),
    path(
        "user/<int:user_id>/view-referral/",
        ViewReferralStringAPIView.as_view(),
        name="api_view_referral_string",
    ),
    path(
        "post_template/document",
        views.create_document_template,
        name="create_document_template",
    ),
    path(
        "validate/credentials",
        views.check_validation,
        name="check_validation",
    ),
    # path(
    #     "user/<int:user_id>/edit-referral/",
    #     EditReferralStringAPIView.as_view(),
    #     name="api_edit_referral_string",
    # ),
    path("check/token/", CheckTokenValidityView.as_view(), name="check-token"),
    path(
        "check/notifications/", CheckNotifications.as_view(), name="check-notifications"
    ),
    path("contact-form/", ContactFormView.as_view(), name="contact-form"),
    path("upload/", PhoneNumberUpload.as_view(), name="upload_phone_numbers"),
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("validate-access-token/", validate_access_token, name="validate_access_token"),
    path("", views.index, name="index"),
    path("privacy/", views.privacy, name="privacy"),
    path("schedule/", views.schedule_api_call, name="schedule_api_call"),
    path(
        "user/schedule/",
        ScheduleHelloView.as_view(),
        name="api_chedulke",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
