from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.product.models import (
    Category, TopLevelCategory, SubCategory, Product, ProductImage, Review,
    Comment, OrderProduct, ProductSize
)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at')
    search_fields = ('name',)
    ordering = ('created_at',)


class TopLevelCategoryAdmin(CategoryAdmin):
    """Admin class for top-level categories (main categories)."""
    list_display = ['name', 'created_at', 'id']
    search_fields = ['name']

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if 'parent' in fields:
            fields.remove('parent')
        return fields

    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=True)


class SubCategoryAdmin(CategoryAdmin):
    list_display = ['name', 'parent', 'created_at', 'id']
    search_fields = ['name']

    # Custom list filter for main categories
    def get_list_filter(self, request):
        return super().get_list_filter(request) + (('parent', admin.RelatedOnlyFieldListFilter),)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=False)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductSizeInline]
    list_display = ('name', 'price', 'category', 'author', 'firm', 'country', 'vendor_code', 'created_at')
    search_fields = ('name', 'firm', 'author__username', 'vendor_code')
    list_filter = ('category', 'firm', 'country', 'created_at')
    prepopulated_fields = {'vendor_code': ('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'created_at')
    search_fields = ('product__name', 'user__username')
    list_filter = ('created_at',)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username')
    list_filter = ('rating', 'created_at')

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'quantity', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at', 'user')
    search_fields = ('product__name', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('product', 'user')


admin.site.register(Product, ProductAdmin)
admin.site.register(TopLevelCategory, TopLevelCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(ProductSize)
