from django.db.models import Avg
from rest_framework import serializers
from apps.product.models import (
    Category, TopLevelCategory, SubCategory, Product, ProductImage, Review,
    Comment
)


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


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return reviews.aggregate(Avg('rating'))['rating__avg']
        return None

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        return product