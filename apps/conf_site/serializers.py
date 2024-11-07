from rest_framework import serializers
from .models import BannerCarousel, Partners, GetConsultation


class BannerCarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerCarousel
        fields = ['id', 'image']


class PartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partners
        fields = ['id', 'image']


class GetConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetConsultation
        fields = ['id', 'full_name', 'phone', 'msg']
