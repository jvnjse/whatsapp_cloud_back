from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import random
import string


def generate_referral_string():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_distributor = models.BooleanField(default=False)
    messaging_feature = models.BooleanField(default=True)
    excel_feature = models.BooleanField(default=False)
    image_feature = models.BooleanField(default=False)
    personalised_feature = models.BooleanField(default=False)
    referral_string = models.CharField(
        max_length=8,
        unique=True,
        default=generate_referral_string,
    )
    parent_user = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )

    # def update_referral_string(self):
    #     self.referral_string = generate_referral_string()
    #     self.save()

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    groups = models.ManyToManyField("auth.Group", related_name="custom_users")
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="custom_users"
    )


# @receiver(post_save, sender=CustomUser)
# def update_referral_string(sender, instance, created, **kwargs):
#     if created:
#         instance.update_referral_string()


class PhoneNumber(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    number = models.CharField(max_length=20)

    def __str__(self):
        return str(self.number)


class WhatsappCredential(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number_id = models.CharField(max_length=30)
    whatsapp_business_id = models.CharField(max_length=30)
    permanent_access_token = models.CharField(max_length=500)

    def __str__(self):
        return str(self.user)


class Template(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    template_name = models.CharField(max_length=30)
    template_image = models.ImageField(upload_to="template_image", null=True)

    def __str__(self):
        return str(self.template_name)

    class Meta:
        unique_together = ("user", "template_name")


class ScheduledAPICall(models.Model):
    api_data = models.TextField()
    scheduled_time = models.DateTimeField()
