from django.db.models import Avg
from rest_framework import serializers
from apps.product.models import (
    Category, TopLevelCategory, SubCategory, Product, ProductImage, Review,
    Comment, OrderProduct, ProductSize
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


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    sizes = ProductSizeSerializer(many=True, required=False)
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
        product = Product.objects.create(**validated_data)
        return product


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