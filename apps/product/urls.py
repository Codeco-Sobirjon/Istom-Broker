from django.urls import path

from apps.product.views import (
    TopLevelCategoryWithSubCategoriesView,
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    CommentListCreateView,
    ReviewListCreateView, ProductCreateIsAuthentification, DistinctProductAttributesView,
)


urlpatterns = [
    path('top-level-categories-with-subcategories/', TopLevelCategoryWithSubCategoriesView.as_view(), name='top-level-categories-with-subcategories'),

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/is/authen/', ProductCreateIsAuthentification.as_view(), name='product-list-create-authen'),


    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-retrieve-update-destroy'),

    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),

    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),

    path('api/distinct-product-attributes/', DistinctProductAttributesView.as_view(), name='distinct-product-attributes'),
]