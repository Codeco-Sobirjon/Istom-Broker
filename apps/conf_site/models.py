from django.db import models
from django.utils.translation import gettext as _


class BannerCarousel(models.Model):
    image = models.ImageField(upload_to='banner/', null=False, blank=False, verbose_name="Изображение")

    class Meta:
        ordering = ["id"]
        verbose_name = _("Изображения для карусели баннеров")
        verbose_name_plural = _("Изображения для карусели баннеров")


class Partners(models.Model):
    image = models.ImageField(upload_to='banner/', null=False, blank=False, verbose_name="Логотип для партнеров")

    class Meta:
        ordering = ["id"]
        verbose_name = _("Наши партнеры")
        verbose_name_plural = _("Наши партнеры")


class GetConsultation(models.Model):
    full_name = models.CharField(_('Полное имя'), max_length=250, null=False, blank=False)
    phone = models.CharField(_('Телефон'), max_length=250, null=False, blank=False)
    msg = models.TextField(null=True, blank=True, verbose_name='Сообщение')

    class Meta:
        ordering = ["id"]
        verbose_name = _("Пришла на консультацию")
        verbose_name_plural = _("Пришла на консультацию")

    def __str__(self):
        return self.full_name
