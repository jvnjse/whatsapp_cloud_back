from django.db import models


# Create your models here.
class PhoneNumber(models.Model):
    number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return str(self.number)
