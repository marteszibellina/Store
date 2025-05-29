"""VIEWSETS for API"""

from django.shortcuts import render


from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as UVS
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

# from api.filters import IngredientFilter, RecipeFilter
from api.pagination import StandartPagination
from api.permissions import (IsAuthorOrReadOnly, IsReadOnly, IsAuthenticated)
from api.serializers import (CategorySerializer, ProductSerializer,
                            ProductImageSerializer,
                            ShoppingCartSerializer,
                            SubCategorySerializer)
from stock.models import (Category, Product,
                          ProductImage, ShoppingCart, SubCategory)

User = get_user_model()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Category viewset."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandartPagination
    lookup_field = 'slug'

    @action(
        detail=True,
        methods=['get'],
        permission_classes=[permissions.AllowAny],
        url_path='subcategory',
    )
    def get_subcategory(self, request, slug):
        """Subcategory viewset."""
        subcategory = SubCategory.objects.filter(category__slug=slug)
        serializer = SubCategorySerializer(subcategory, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_subcategory_detail(self, category_slug, subcategory_slug):
    """Subcategory detail viewset."""

    try:
        subcategory = SubCategory.objects.get(
            slug=subcategory_slug,
            category__slug=category_slug,
        )
    except SubCategory.DoesNotExist:
        return Response({'detail': 'Not found'},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = SubCategorySerializer(subcategory)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_product_detail(self, category_slug, subcategory_slug, product_slug):
    """Product detail viewset."""

    try:
        product = Product.objects.get(
            slug=product_slug,
            subcategory__slug=subcategory_slug,
            subcategory__category__slug=category_slug
        )
    except Product.DoesNotExist:
        return Response({'detail': 'Not found'},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)
    return Response(serializer.data)


    # @action(
    #     detail=True,
    #     methods=['get'],
    #     permission_classes=[IsReadOnly],
    #     url_path='product',
    # )
    # def get_product(self, request, slug):
    #     """Product viewset."""
    #     product = Product.objects.filter(subcategory_slug=slug)
    #     serializer = ProductSerializer(product, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(
    #     detail=True,
    #     methods=['get'],
    #     permission_classes=[IsReadOnly],
    #     url_path='product_image',
    # )
    # def get_product_image(self, request, slug):
    #     """ProductImage viewset."""
    #     product_image = ProductImage.objects.filter(product_slug=slug)
    #     serializer = ProductImageSerializer(product_image, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
