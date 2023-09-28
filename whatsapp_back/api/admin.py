from django.contrib import admin
from .models import PhoneNumber, CustomUser, WhatsappCredential

# Register your models here.
admin.site.register(PhoneNumber)
admin.site.register(CustomUser)
admin.site.register(WhatsappCredential)
