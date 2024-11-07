from django.urls import path
from apps.conf_site.views import BannerCarouselListView, PartnersListView, GetConsultationListView

urlpatterns = [
    path('banners/', BannerCarouselListView.as_view(), name='banner-carousel-list'),
    path('partners/', PartnersListView.as_view(), name='partners-list'),
    path('consultations/', GetConsultationListView.as_view(), name='get-consultation-list'),
]
