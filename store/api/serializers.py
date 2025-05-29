"""SERIALIZERS for API"""

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers, validators

from api.fields import Base64ImageField

from stock.models import (Category, Product,
    ProductImage, ShoppingCart, SubCategory)

from stock.constants import (CATEGORY_NAME_LENGTH, CATEGORY_SLUG_LENGTH,
       PRODUCT_NAME_LENGTH, PRODUCT_SLUG_LENGTH,
       PRODUCT_PRICE_MAX_DIGITS, PRODUCT_PRICE_DECIMAL_PLACES,
       TEXT_SLICE,)

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        """Meta class for CategorySerializer."""
        model = Category
        fields = ('name', 'slug', 'image',)


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for ProductImage model."""

    image = Base64ImageField()

    class Meta:
        """Meta class for ProductImageSerializer."""
        model = ProductImage
        fields = ('id', 'product', 'image',)


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""

    image = ProductImageSerializer(many=True, read_only=True,
                                   source='product_images')

    class Meta:
        """Meta class for ProductSerializer."""
        model = Product
        fields = ('id', 'name', 'slug', 'price', 'image')


class SubCategorySerializer(serializers.ModelSerializer):
    """Serializer for SubCategory model."""

    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        """Meta class for SubCategorySerializer."""
        model = SubCategory
        fields = ('name', 'slug', 'image', 'category', 'products',)


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Serializer for ShoppingCart model."""

    user = serializers.ReadOnlyField(source='user.username')
    product = serializers.ReadOnlyField(source='product.name')
    price = serializers.DecimalField(source='product.price',
                         max_digits=PRODUCT_PRICE_MAX_DIGITS,
                         decimal_places=PRODUCT_PRICE_DECIMAL_PLACES)

    class Meta:
        """Meta class for ShoppingCartSerializer."""
        model = ShoppingCart
        fields = ('user', 'product', 'quantity', 'price',)
