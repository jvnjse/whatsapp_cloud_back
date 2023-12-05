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
    path("users/", UserListView.as_view(), name="user-list"),
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
        "post_template/image",
        views.create_image_template,
        name="create_image_template",
    ),
    path(
        "upload/sent",
        views.excel_sent_message,
        name="excel_sent_message",
    ),
    path(
        "upload/sent/images",
        views.excel_sent_message_images,
        name="excel_sent_message_images",
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
    # path(
    #     "user/<int:user_id>/edit-referral/",
    #     EditReferralStringAPIView.as_view(),
    #     name="api_edit_referral_string",
    # ),
    path("upload/", PhoneNumberUpload.as_view(), name="upload_phone_numbers"),
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("validate-access-token/", validate_access_token, name="validate_access_token"),
    path("", views.index, name="index"),
    path("privacy/", views.privacy, name="privacy"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
