from django.contrib import admin
from .models import BannerCarousel, Partners, GetConsultation


@admin.register(BannerCarousel)
class BannerCarouselAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
    ordering = ['id']


@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
    ordering = ['id']


@admin.register(GetConsultation)
class GetConsultationAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'msg')
    ordering = ['id']
