import django_filters
from apps.product.models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
            'brand': ['exact', 'icontains'],
            'size': ['exact', 'icontains'],
            'volume': ['exact', 'icontains'],
            'size_of_brackets': ['exact', 'icontains'],
            'the_height_of_the_closing_barckets': ['exact', 'icontains'],
            'outer_diameter_of_the_head': ['exact', 'icontains'],
            'firm': ['exact', 'icontains'],
            'country': ['exact', 'icontains'],
            'vendor_code': ['exact', 'icontains'],
            'degree_of_extensibility': ['exact', 'icontains'],
            'color': ['exact', 'icontains'],
            'is_discount': ['exact'],
            'is_new_product': ['exact'],
            'in_stock': ['exact'],
        }
