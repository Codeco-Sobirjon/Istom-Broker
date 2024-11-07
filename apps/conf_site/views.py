from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import BannerCarousel, Partners, GetConsultation
from .serializers import BannerCarouselSerializer, PartnersSerializer, GetConsultationSerializer


class BannerCarouselListView(APIView):
    @swagger_auto_schema(
        operation_summary="Get all banner images",
        tags=['configuration main site'],
        responses={200: BannerCarouselSerializer(many=True)}
    )
    def get(self, request):
        banners = BannerCarousel.objects.all()
        serializer = BannerCarouselSerializer(banners, many=True)
        return Response(serializer.data)


class PartnersListView(APIView):
    @swagger_auto_schema(
        operation_summary="Get all partner logos",
        tags=['configuration main site'],
        responses={200: PartnersSerializer(many=True)}
    )
    def get(self, request):
        partners = Partners.objects.all()
        serializer = PartnersSerializer(partners, many=True)
        return Response(serializer.data)


class GetConsultationListView(APIView):
    @swagger_auto_schema(
        operation_summary="Get all consultation requests",
        tags=['configuration main site'],
        responses={200: GetConsultationSerializer(many=True)}
    )
    def get(self, request):
        consultations = GetConsultation.objects.all()
        serializer = GetConsultationSerializer(consultations, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a consultation request",
        tags=['configuration main site'],
        request_body=GetConsultationSerializer,
        responses={
            201: GetConsultationSerializer,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = GetConsultationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
