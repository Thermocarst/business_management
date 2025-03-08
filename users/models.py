from django.contrib.auth.models import AbstractUser
from django.db import models
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _


# Create your models here.

class User(AbstractUser):

    class Roles(models.TextChoices):
        COMPANY_OWNER = "COMPANY_OWNER", "Company owner"
        ADMINISTRATOR = "ADMINISTRATOR", "Administrator"
        EMPLOYEE = "EMPLOYEE", "Employee"
        NULL = "NULL", "null"

    def upload_img(self, file_name: str):
        return f"users/avatar/{self.username}.webp"

    role: int = models.CharField(max_length=50, choices=Roles.choices, default=Roles.NULL,
                                  verbose_name=_("role"))
    image: str = ResizedImageField(force_format="WEBP",
                                   quality=75,
                                   size=(500, 500),
                                   crop=["middle", "center"],
                                   upload_to=upload_img,
                                   verbose_name=_("image"),
                                   help_text="500x500", null=True, blank=True)

    def __str__(self):
        return self.username


class Company(models.Model):

    title: str = models.CharField(max_length=100, verbose_name=_("title"))
    user: id = models.ManyToManyField(User, verbose_name=_("user"), related_name="companies")

    def __str__(self):
        return self.title
    