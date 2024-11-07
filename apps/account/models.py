# yourapp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class CustomUser(AbstractUser):
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Адрес"))
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Телефон"))
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_("Аватар"))

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return self.username

