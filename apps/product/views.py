import json

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict

from apps.product.filters import ProductFilter
from apps.product.models import (
    Category, Product, OrderProduct, ProductImage, ProductSize
)
from apps.product.pagination import ProductPagination
from apps.product.serializers import (
    TopLevelCategoryWithSubCategoriesSerializer,
    ProductSerializer, CommentSerializer, ReviewSerializer, CreateOrderProductSerializer, OrderProductSerializer,
    ProductDetailSerializer
)
from apps.product.utils import get_distinct_product_attributes


class TopLevelCategoryWithSubCategoriesView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        tags=['category'],
        operation_description="Retrieve all top-level categories along with their subcategories.",
        responses={
            200: TopLevelCategoryWithSubCategoriesSerializer(many=True),
            404: openapi.Response('Not Found'),
        }
    )
    def get(self, request):

        top_level_categories = Category.objects.select_related('parent').filter(
            parent__isnull=True
        )
        serializer = TopLevelCategoryWithSubCategoriesSerializer(top_level_categories, many=True,
                                                                 context={'request': request})
        return Response(serializer.data)


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class GetCategoryProductView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['category'],
        operation_description="Retrieve all category's product",
        responses={
            200: ProductSerializer(many=True),
            404: openapi.Response('Not Found'),
        }
    )
    def get(self, request, *args, **kwargs):
        queryset = get_object_or_404(Category, id=kwargs.get('id'))
        product_list = Product.objects.select_related('category').filter(
            category=queryset
        )
        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(product_list, request, view=self)

        serializer = ProductSerializer(paginated_products, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class ProductListCreateView(APIView):
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ProductFilter

    @swagger_auto_schema(
        operation_summary="List all products without authentication",
        tags=["product's not authentication"],
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description="Filter by category ID",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('brand', openapi.IN_QUERY, description="Filter by brand name (exact match)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('size', openapi.IN_QUERY, description="Filter by size (exact match)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('volume', openapi.IN_QUERY, description="Filter by volume (exact match)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('size_of_brackets', openapi.IN_QUERY,
                              description="Filter by size of brackets (exact match)", type=openapi.TYPE_STRING),
            openapi.Parameter('the_height_of_the_closing_barckets', openapi.IN_QUERY,
                              description="Filter by height of closing brackets (exact match)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('outer_diameter_of_the_head', openapi.IN_QUERY,
                              description="Filter by outer diameter of the head (exact match)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('firm', openapi.IN_QUERY, description="Filter by firm name (exact match)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('country', openapi.IN_QUERY, description="Filter by country name (exact match)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('vendor_code', openapi.IN_QUERY, description="Filter by vendor code (exact match)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('degree_of_extensibility', openapi.IN_QUERY,
                              description="Filter by degree of extensibility (exact match)", type=openapi.TYPE_STRING),
            openapi.Parameter('color', openapi.IN_QUERY, description="Filter by color (exact match)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('is_discount', openapi.IN_QUERY,
                              description="Filter by discount availability (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('is_new_product', openapi.IN_QUERY,
                              description="Filter by new product status (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('in_stock', openapi.IN_QUERY, description="Filter by stock availability (true/false)",
                              type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: ProductSerializer(many=True)},
    )
    def get(self, request):
        products = Product.objects.all()
        filtered_queryset = self.filterset_class(request.GET, queryset=products)
        paginator = ProductPagination()
        paginated_products = paginator.paginate_queryset(filtered_queryset.qs, request)
        serializer = ProductSerializer(paginated_products, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class ProductCreateIsAuthentification(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List all products ",
        tags=['product'],
        responses={200: ProductSerializer(many=True)},
    )
    def get(self, request):
        products = Product.objects.select_related('author').filter(
            author=request.user
        )
        paginator = ProductPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(paginated_products, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a new product",
        tags=['product'],
        request_body=ProductSerializer,
        responses={201: ProductSerializer},
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveUpdateDestroyView(APIView):

    @swagger_auto_schema(
        operation_summary="Retrieve a product",
        tags=['product'],
        responses={200: ProductSerializer, 404: "Not Found"},
    )
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductDetailSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Update a product",
        tags=['product'],
        request_body=ProductSerializer,
        responses={200: ProductSerializer, 404: "Not Found"},
    )
    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Delete a product",
        tags=['product'],
        responses={204: "No Content", 404: "Not Found"},
    )
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a new comment",
        tags=['comment'],
        request_body=CommentSerializer,
        responses={201: CommentSerializer},
    )
    def post(self, request):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            comment = serializer.save()
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a new review",
        tags=['review'],
        request_body=ReviewSerializer,
        responses={201: ReviewSerializer},
    )
    def post(self, request):
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            review = serializer.save()
            return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DistinctProductAttributesView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary="Get distinct product attributes",
        tags=["product attributes"],
        responses={
            200: openapi.Response(
                description="Distinct product attributes retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'brands': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                        'sizes': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                        'volumes': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                        'sizes_of_brackets': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                        'heights_of_closing_brackets': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                        'outer_diameters_of_heads': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                        'countries': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                        'firms': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                        'degree_of_extensibility': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                        'color': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                    }
                )
            )
        }
    )
    def get(self, request):
        distinct_attributes = get_distinct_product_attributes()
        return Response(distinct_attributes)


class CreateOrderProductView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a order",
        tags=['order'],
        request_body=CreateOrderProductSerializer,
        responses={201: CreateOrderProductSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = CreateOrderProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order_products = serializer.save()
            return Response({"message": "Order products created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrderProductListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="User gets order product",
        tags=['order'],
        responses={200: ProductSerializer, 404: "Not Found"},
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        order_products = OrderProduct.objects.filter(user=user)

        paginator = PageNumberPagination()
        paginated_order_products = paginator.paginate_queryset(order_products, request)

        serializer = OrderProductSerializer(paginated_order_products, many=True)
        return paginator.get_paginated_response(serializer.data)


class WeeklyOrderProductStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    class CustomPagination(PageNumberPagination):
        page_size = 4
        page_size_query_param = 'page_size'
        max_page_size = 100

    @swagger_auto_schema(
        operation_summary="Statistics of product sales by week",
        tags=['order'],
        responses={200: 'A list of product sales statistics for the last 7 days', 404: "Not Found"},
    )
    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        seven_days_ago = today + timedelta(days=7)

        orders = OrderProduct.objects.select_related('user').filter(
            user=request.user
        ).filter(
            created_at__gte=today, created_at__lte=seven_days_ago
        )

        weekly_orders = defaultdict(lambda: defaultdict(int))

        for order in orders:
            product = order.product
            order_date = order.created_at.date()
            weekly_orders[product][order_date] += order.quantity

        all_dates = [today + timedelta(days=i) for i in range(8)]

        result = []
        for product, daily_orders in weekly_orders.items():
            weekly_data = []
            for date in all_dates:
                weekly_data.append({
                    "date": str(date),
                    "quantity": daily_orders.get(date, 0)
                })

            result.append({
                "product": ProductSerializer(product, context={'request': request}).data,
                "weekly_order": weekly_data
            })

        paginator = self.CustomPagination()
        paginated_result = paginator.paginate_queryset(result, request)

        return paginator.get_paginated_response(paginated_result)

