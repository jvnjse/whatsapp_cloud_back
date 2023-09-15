from django.contrib import admin
from .models import PhoneNumber, CustomUser

# Register your models here.
admin.site.register(PhoneNumber)
admin.site.register(CustomUser)
