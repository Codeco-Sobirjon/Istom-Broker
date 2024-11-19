import json
import os
from urllib.parse import urlparse

from django.core.files.base import ContentFile
from django.db.models import Avg
from rest_framework import serializers
from apps.product.models import (
    Category, TopLevelCategory, SubCategory, Product, ProductImage, Review,
    Comment, OrderProduct, ProductSize
)
import requests


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name']


class TopLevelCategoryWithSubCategoriesSerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(many=True, source='subcategories')

    class Meta:
        model = TopLevelCategory
        fields = ['id', 'name', 'sub_category']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    class Meta:
        model = Product
        fields = ['id', 'name', 'vendor_code', 'images', 'uploaded_images', 'author',]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        user = self.context.get('request').user
        product = Product.objects.create(**validated_data, author=user)
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)
        return product


class ProductDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    sizes = ProductSizeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return reviews.aggregate(Avg('rating'))['rating__avg']
        return None


class OrderProductListSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    total = serializers.IntegerField()


class CreateOrderProductSerializer(serializers.Serializer):
    order_products_list = OrderProductListSerializer(many=True)

    def create(self, validated_data):
        user = self.context['request'].user
        order_products_list = validated_data['order_products_list']
        created_orders = []

        for order_data in order_products_list:
            product_id = order_data['product_id']
            quantity = order_data['quantity']
            total = order_data['total']

            product = Product.objects.get(id=product_id)
            order_product = OrderProduct.objects.create(
                user=user,
                product=product,
                quantity=quantity,
                total=total,
                status='processing',
            )
            created_orders.append(order_product)

        return created_orders


class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'product_name', 'quantity', 'status', 'total', 'created_at']