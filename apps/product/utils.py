from django.db.models import Q

from apps.product.models import Product


def get_distinct_product_attributes():

    distinct_brands = set()
    distinct_sizes = set()
    distinct_volumes = set()
    distinct_sizes_of_brackets = set()
    distinct_heights_of_closing_brackets = set()
    distinct_outer_diameters_of_heads = set()
    distinct_countries = set()
    distinct_firms = set()
    distinct_degree_of_extensibility = set()
    distinct_color = set()

    products = Product.objects.all()

    for product in products:
        if product.brand:
            distinct_brands.add(product.brand)
        if product.size:
            distinct_sizes.add(product.size)
        if product.volume:
            distinct_volumes.add(product.volume)
        if product.size_of_brackets:
            distinct_sizes_of_brackets.add(product.size_of_brackets)
        if product.the_height_of_the_closing_barckets:
            distinct_heights_of_closing_brackets.add(product.the_height_of_the_closing_barckets)
        if product.outer_diameter_of_the_head:
            distinct_outer_diameters_of_heads.add(product.outer_diameter_of_the_head)
        if product.country:
            distinct_countries.add(product.country)
        if product.firm:
            distinct_firms.add(product.firm)
        if product.degree_of_extensibility:
            distinct_degree_of_extensibility.add(product.degree_of_extensibility)
        if product.color:
            distinct_color.add(product.color)


    return {
        'brands': list(distinct_brands),
        'sizes': list(distinct_sizes),
        'volumes': list(distinct_volumes),
        'sizes_of_brackets': list(distinct_sizes_of_brackets),
        'heights_of_closing_brackets': list(distinct_heights_of_closing_brackets),
        'outer_diameters_of_heads': list(distinct_outer_diameters_of_heads),
        'countries': list(distinct_countries),
        'firms': list(distinct_firms),
        'degree_of_extensibility': list(distinct_degree_of_extensibility),
        'color': list(distinct_color),
    }