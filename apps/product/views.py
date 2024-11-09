from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.product.filters import ProductFilter
from apps.product.models import (
    Category, TopLevelCategory, SubCategory, Product, ProductImage, Review,
    Comment
)
from apps.product.pagination import ProductPagination
from apps.product.serializers import (
    TopLevelCategoryWithSubCategoriesSerializer,
    ProductSerializer, CommentSerializer, ReviewSerializer
)
from apps.product.utils import get_distinct_product_attributes


class TopLevelCategoryWithSubCategoriesView(APIView):

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


class ProductListCreateView(APIView):
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ProductFilter  # Use the filter set defined earlier

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
        products = Product.objects.all()  # This must be a queryset
        filtered_queryset = self.filterset_class(request.GET, queryset=products)
        paginator = ProductPagination()
        paginated_products = paginator.paginate_queryset(filtered_queryset.qs, request)
        serializer = ProductSerializer(paginated_products, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class ProductCreateIsAuthentification(APIView):
    # permission_classes = [IsAuthenticated]

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
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
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
            serializer = ProductSerializer(product, context={'request': request})
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
    # permission_classes = [IsAuthenticated]

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
    # permission_classes = [IsAuthenticated]

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
    # permission_classes = [AllowAny]

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