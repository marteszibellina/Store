"""Stock models."""

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

from stock.constants import (
    CATEGORY_NAME_LENGTH, CATEGORY_SLUG_LENGTH,
    PRODUCT_NAME_LENGTH, PRODUCT_SLUG_LENGTH,
    PRODUCT_PRICE_MAX_DIGITS, PRODUCT_PRICE_DECIMAL_PLACES,
    TEXT_SLICE,)

class Category(models.Model):
    """Category model."""

    name = models.CharField(max_length=CATEGORY_NAME_LENGTH)
    slug = models.SlugField(max_length=CATEGORY_SLUG_LENGTH,
                            unique=True)
    image = models.ImageField(upload_to='category/images',
                              blank=True)

    def __str__(self):
        """Return category name."""
        return self.name[:TEXT_SLICE]

    class Meta:
        """Meta-Class for Category."""
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']


class SubCategory(models.Model):
    """SubCategory model."""

    name = models.CharField(max_length=CATEGORY_NAME_LENGTH)
    slug = models.SlugField(max_length=CATEGORY_SLUG_LENGTH,
                            unique=True)
    image = models.ImageField(upload_to='subcategory/images',)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='subcategories')

    def __str__(self):
        """Return subcategory name."""
        return f'{self.category.name}[{TEXT_SLICE}]:{self.name}[:{TEXT_SLICE}]'

    class Meta:
        """Meta-Class for SubCategory."""
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'
        ordering = ['name']


class ProductImage(models.Model):
    """ProductImage model."""

    image = models.ImageField('product-images',
                              blank=True,
                              upload_to='product/images')
    order = models.PositiveSmallIntegerField(default=0,
                                             verbose_name='Order')
    product = models.ForeignKey('Product', on_delete=models.CASCADE,
                                related_name='product_images')

    def __str__(self):
        """Return product name."""
        return f'{self.product.name}: Order {self.order}'

    class Meta:
        """Meta-Class for ProductImage."""
        verbose_name = 'ProductImage'
        verbose_name_plural = 'ProductImages'
        ordering = ['order']


class Product(models.Model):
    """Product model."""

    name = models.CharField(max_length=PRODUCT_NAME_LENGTH)
    slug = models.SlugField(max_length=PRODUCT_SLUG_LENGTH,
                            unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,
                                    related_name='products')
    price = models.DecimalField(max_digits=PRODUCT_PRICE_MAX_DIGITS,
                                decimal_places=PRODUCT_PRICE_DECIMAL_PLACES)

    def __str__(self):
        """Return product name."""
        return f'{self.name}:{self.price} of {self.category.name}:{self.subcategory.name}'

    class Meta:
        """Meta-Class for Product."""
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    @property
    def category(self):
        """Return category name."""
        return self.subcategory.category


class ShoppingCart(models.Model):
    """ShoppingCart model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        """Return product name."""
        return f'{self.user.username}:{self.product.name}:{self.quantity}:{self.price}'
