from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class PhoneNumber(models.Model):
    number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return str(self.number)
