from django.contrib import admin
from .models import (
    PhoneNumber,
    CustomUser,
    WhatsappCredential,
    Template,
    ContactForm,
    Notification,
    PlanPurchase,
    Blog,
    ContactGroup,
)

# Register your models here.
admin.site.register(Blog)
admin.site.register(PhoneNumber)
admin.site.register(CustomUser)
admin.site.register(WhatsappCredential)
admin.site.register(Template)
admin.site.register(ContactForm)
admin.site.register(Notification)
admin.site.register(PlanPurchase)
admin.site.register(ContactGroup)
